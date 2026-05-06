import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState, useMemo, useRef, forwardRef } from 'react';
import html2canvas from 'html2canvas';
import LatexRenderer from '../components/LatexRenderer';
import BacCountdown from '../components/BacCountdown';
import {
  CheckCircle, XCircle, RotateCcw, Zap,
  ChevronDown, ChevronUp, Calendar, Share2,
  X, Check, Copy, Loader2, Download,
} from 'lucide-react';

const MOALIM_URL = 'https://moalim.online';
const DIAG_URL  = `${MOALIM_URL}/bac-diagnostic`;

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

// ── Shareable card (captured by html2canvas) ────────────────────────────────

interface ShareCardProps {
  avg: number;
  mentionFr: string;
  mentionColor: string;
  massarCode: string;
  isAdmis: boolean;
  subjects: Array<{ ar: string; short: string; note: number }>;
}

const BacResultShareCard = forwardRef<HTMLDivElement, ShareCardProps>(
  function BacResultShareCardImpl({ avg, mentionFr, mentionColor, massarCode, isAdmis, subjects }, ref) {
    const col = avg >= 10 ? '#4ade80' : '#f87171';
    return (
      <div ref={ref} style={{
        width: 480, fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif',
        background: 'linear-gradient(145deg,#070718 0%,#0d0d28 60%,#130d2e 100%)',
        color: 'white', padding: 28, position: 'relative', overflow: 'hidden',
      }}>
        {/* Glow */}
        <div style={{ position:'absolute', top:-60, left:'50%', transform:'translateX(-50%)', width:340, height:200, borderRadius:'50%', background:'rgba(99,102,241,0.22)', filter:'blur(55px)' }} />
        {/* Header */}
        <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:18, position:'relative' }}>
          <div>
            <div style={{ fontSize:9, color:'rgba(255,255,255,0.3)', textTransform:'uppercase', letterSpacing:2 }}>وزارة التربية الوطنية · MASSAR</div>
            <div style={{ fontSize:13, fontWeight:800, marginTop:3 }}>نتائج الباكالوريا — Session Normale 2026</div>
          </div>
          <div style={{ textAlign:'right' }}>
            <div style={{ fontSize:8, color:'rgba(255,255,255,0.28)' }}>رمز مسار</div>
            <div style={{ fontSize:11, fontFamily:'monospace', fontWeight:700, color:'rgba(255,255,255,0.6)', marginTop:2 }}>{massarCode}</div>
          </div>
        </div>
        {/* Divider */}
        <div style={{ height:1, background:'rgba(255,255,255,0.08)', marginBottom:16, position:'relative' }} />
        {/* Score circle + info */}
        <div style={{ display:'flex', alignItems:'center', gap:20, marginBottom:18, position:'relative' }}>
          <div style={{ width:110, height:110, borderRadius:'50%', border:`3px solid ${col}`, display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', flexShrink:0, background:'rgba(255,255,255,0.04)', boxShadow:`0 0 24px ${col}44` }}>
            <div style={{ fontSize:32, fontWeight:900, color:col, lineHeight:1 }}>{avg.toFixed(2)}</div>
            <div style={{ fontSize:11, color:'rgba(255,255,255,0.4)', fontWeight:600, marginTop:2 }}>/ 20</div>
          </div>
          <div style={{ flex:1 }}>
            <div style={{ fontSize:10, color:'rgba(255,255,255,0.35)', textTransform:'uppercase', letterSpacing:1.2, marginBottom:4 }}>المستوى</div>
            <div style={{ fontSize:12, fontWeight:600, marginBottom:6 }}>الثانية باكالوريا علوم فيزيائية</div>
            <div style={{ fontSize:10, color:'rgba(255,255,255,0.35)', textTransform:'uppercase', letterSpacing:1.2, marginBottom:3 }}>النتيجة</div>
            <div style={{ fontSize:14, fontWeight:800, color:col }}>
              {isAdmis ? 'ناجح(ة)' : 'غير ناجح'} · Mention : {mentionFr}
            </div>
          </div>
        </div>
        {/* Subject table */}
        <div style={{ background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)', borderRadius:12, padding:'10px 14px', marginBottom:18, position:'relative' }}>
          <div style={{ fontSize:10, color:'#f87171', fontWeight:700, marginBottom:8, textAlign:'right' }}>: بيان النقط حسب المادة</div>
          {subjects.map((s, i) => (
            <div key={i} style={{ display:'flex', justifyContent:'space-between', alignItems:'center', padding:'5px 0', borderBottom: i < subjects.length-1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
              <div style={{ fontSize:12, fontWeight:700, color: s.note >= 14 ? '#4ade80' : s.note >= 10 ? '#fbbf24' : '#f87171' }}>{s.note.toFixed(2)}</div>
              <div style={{ textAlign:'right' }}>
                <div style={{ fontSize:12, fontWeight:500 }}>{s.ar}</div>
                <div style={{ fontSize:9, color:'rgba(255,255,255,0.25)' }}>{s.short}</div>
              </div>
            </div>
          ))}
        </div>
        {/* CTA */}
        <div style={{ background:'rgba(99,102,241,0.18)', border:'1px solid rgba(99,102,241,0.35)', borderRadius:12, padding:'10px 14px', position:'relative' }}>
          <div style={{ fontSize:13, fontWeight:700, marginBottom:4 }}>أنت كم حصلت في الباكالوريا 2026؟</div>
          <div style={{ fontSize:11, color:'rgba(255,255,255,0.55)', marginBottom:6 }}>اختبر نتيجتك في 20 سؤال فقط · مجاني</div>
          <div style={{ fontSize:12, fontWeight:800, color:'#a5b4fc' }}>{DIAG_URL.replace('https://','')}</div>
        </div>
        {/* Footer */}
        <div style={{ marginTop:14, display:'flex', justifyContent:'space-between', alignItems:'center', fontSize:10, color:'rgba(255,255,255,0.2)', position:'relative' }}>
          <div>Estimation BAC · non officiel</div>
          <div style={{ fontWeight:700, color:'rgba(165,180,252,0.5)' }}>moalim.online</div>
        </div>
      </div>
    );
  }
);

// ── Share modal ──────────────────────────────────────────────────────────────

interface ShareModalProps extends ShareCardProps {
  onClose: () => void;
}

function BacShareModal({ onClose, ...cardProps }: ShareModalProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [generating, setGenerating] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [fileShareUnsupported, setFileShareUnsupported] = useState(false);

  const shareText =
    `🎓 حصلت على ${cardProps.avg.toFixed(2)}/20 في الباكالوريا 2026!\n` +
    `Mention : ${cardProps.mentionFr}\n\n` +
    `أنت كم حصلت؟ اختبر نتيجتك في 20 سؤال 👇\n${DIAG_URL}`;
  const shareTextNoUrl =
    `🎓 حصلت على ${cardProps.avg.toFixed(2)}/20 في الباكالوريا 2026!\n` +
    `Mention : ${cardProps.mentionFr}\n\n` +
    `أنت كم حصلت في الباكالوريا 2026؟`;

  const fileName = `bac-2026-resultats-${cardProps.massarCode}.png`;

  const generatePng = async (): Promise<Blob | null> => {
    if (!cardRef.current) return null;
    const canvas = await html2canvas(cardRef.current, {
      backgroundColor: null, scale: 2, useCORS: true, logging: false,
    });
    return new Promise<Blob | null>((resolve) =>
      canvas.toBlob((blob) => resolve(blob), 'image/png', 1)
    );
  };

  const downloadImage = async (preBlob?: Blob) => {
    const blob = preBlob ?? (await generatePng());
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fileName;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    setDownloaded(true); setTimeout(() => setDownloaded(false), 2500);
  };

  const shareNative = async () => {
    setGenerating(true); setFileShareUnsupported(false);
    try {
      const blob = await generatePng();
      if (!blob) return;
      const file = new File([blob], fileName, { type: 'image/png' });
      const nav: any = navigator;
      const shareData = { title: 'Moalim — Résultat BAC 2026', text: shareTextNoUrl, url: DIAG_URL, files: [file] };
      if (nav.canShare && nav.canShare({ files: [file] })) {
        await nav.share(shareData); onClose();
      } else {
        await downloadImage(blob); setFileShareUnsupported(true);
      }
    } catch (e) { console.warn('Share failed:', e); }
    finally { setGenerating(false); }
  };

  const handleDownload = async () => {
    setGenerating(true);
    try { await downloadImage(); } finally { setGenerating(false); }
  };

  const copyText = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true); setTimeout(() => setCopied(false), 2000);
    } catch { window.prompt('Copie ce message :', shareText); }
  };

  const handleNetworkClick = async (e: React.MouseEvent<HTMLAnchorElement>, url: string) => {
    e.preventDefault();
    try { await navigator.clipboard.writeText(shareText); } catch { /* noop */ }
    await downloadImage();
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const networks = [
    { name: 'WhatsApp', color: 'bg-[#25D366] hover:bg-[#1ebe5d]', url: `https://wa.me/?text=${encodeURIComponent(shareText)}` },
    { name: 'Facebook', color: 'bg-[#1877F2] hover:bg-[#0f63d1]', url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(DIAG_URL)}&quote=${encodeURIComponent(shareTextNoUrl)}` },
    { name: 'Instagram / TikTok', color: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:opacity-90', url: '#' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto" onClick={onClose}>
      <div onClick={(e) => e.stopPropagation()} className="bg-[#0d0d24] border border-white/[.12] rounded-2xl shadow-2xl w-full max-w-md overflow-hidden my-4">

        {/* Modal header */}
        <div className="bg-[#12122e] border-b border-white/[.08] px-5 py-4 flex items-start justify-between">
          <div>
            <h3 className="text-sm font-bold text-white">Partager mes résultats</h3>
            <p className="text-[10px] text-white/40 mt-0.5">
              BAC 2026 · {cardProps.avg.toFixed(2)}/20 · Mention {cardProps.mentionFr}
            </p>
          </div>
          <button onClick={onClose} className="p-1 text-white/50 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Card preview */}
        <div className="px-4 pt-4 pb-2">
          <a href={DIAG_URL} target="_blank" rel="noopener noreferrer"
            className="block rounded-xl overflow-hidden shadow-xl border border-white/[.08]">
            <BacResultShareCard ref={cardRef} {...cardProps} />
          </a>
          <p className="text-[10px] text-center text-white/30 mt-2">
            Image générée · Lien vers{' '}
            <span className="font-semibold text-indigo-400">moalim.online/bac-diagnostic</span>
          </p>
        </div>

        {/* Action buttons */}
        <div className="px-5 pt-2 pb-2 space-y-2">
          <button onClick={shareNative} disabled={generating}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl text-sm font-bold hover:opacity-90 transition-all disabled:opacity-60">
            {generating
              ? <><Loader2 className="w-4 h-4 animate-spin" /> Génération de l'image…</>
              : <><Share2 className="w-4 h-4" /> Partager l'image + texte</>
            }
          </button>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={handleDownload} disabled={generating}
              className="flex items-center justify-center gap-1.5 px-3 py-2.5 bg-white/[.06] border border-white/10 rounded-xl text-xs font-semibold text-white/75 hover:border-indigo-400 hover:text-indigo-300 transition-colors disabled:opacity-60">
              {downloaded
                ? <><Check className="w-3.5 h-3.5 text-emerald-400" /><span className="text-emerald-400">Téléchargée</span></>
                : <><Download className="w-3.5 h-3.5" /> Télécharger l'image</>
              }
            </button>
            <button onClick={copyText}
              className="flex items-center justify-center gap-1.5 px-3 py-2.5 bg-white/[.06] border border-white/10 rounded-xl text-xs font-semibold text-white/75 hover:border-indigo-400 hover:text-indigo-300 transition-colors">
              {copied
                ? <><Check className="w-3.5 h-3.5 text-emerald-400" /><span className="text-emerald-400">Texte copié</span></>
                : <><Copy className="w-3.5 h-3.5" /> Copier le texte</>
              }
            </button>
          </div>
          {fileShareUnsupported && (
            <p className="text-[11px] text-amber-200 bg-amber-500/10 border border-amber-400/25 rounded-lg px-3 py-2">
              Image téléchargée ! Ton navigateur ne supporte pas le partage de fichier — joins-la manuellement.
            </p>
          )}
        </div>

        {/* Network links */}
        <div className="px-5 py-4">
          <p className="text-[10px] font-semibold text-white/40 uppercase tracking-wider mb-2">Ou directement sur un réseau</p>
          <div className="grid grid-cols-3 gap-2">
            {networks.map((net) => (
              <a key={net.name} href={net.url}
                onClick={(e) => handleNetworkClick(e, net.url)}
                target="_blank" rel="noopener noreferrer"
                className={`flex items-center justify-center px-2 py-2.5 rounded-xl ${net.color} text-white text-[11px] font-semibold transition-all hover:shadow-md`}>
                {net.name}
              </a>
            ))}
          </div>
          <p className="text-[10px] text-white/25 text-center mt-2">
            Instagram / TikTok : l'image se télécharge, puis joins-la à ton post
          </p>
        </div>
      </div>
    </div>
  );
}


export default function DiagnosticBacResults() {
  const location = useLocation();
  const navigate = useNavigate();
  const results: Results | null = location.state?.results ?? null;
  const [showDetails, setShowDetails] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
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

  const shareSubjects = SUBJECTS.map(s => ({
    ar: s.ar, short: s.short,
    note: by_subject[s.key] ? subjectNote(by_subject[s.key].pct) : 0,
  }));

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

          {/* ── Share button ── */}
          <button
            onClick={() => setShowShareModal(true)}
            className="w-full py-3 bg-white/[.05] border border-white/10 rounded-xl text-white/70 text-sm font-semibold flex items-center justify-center gap-2 hover:bg-white/[.09] hover:text-white active:scale-[.98] transition-all"
          >
            <Share2 className="w-4 h-4" />
            Partager mes résultats · شارك نتيجتك
          </button>

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

      {showShareModal && (
        <BacShareModal
          onClose={() => setShowShareModal(false)}
          avg={bac_note_predicted}
          mentionFr={mention.fr}
          mentionColor={mention.tw}
          massarCode={massarCode}
          isAdmis={isAdmis}
          subjects={shareSubjects}
        />
      )}
    </div>
  );
}
