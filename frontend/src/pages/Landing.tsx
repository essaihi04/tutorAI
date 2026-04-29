import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import ConcoursCalendarPopup from '../components/ConcoursCalendarPopup';
import MoalimChatbot from '../components/MoalimChatbot';
import {
  Sparkles, Brain, Zap, Trophy, ArrowRight, Check, Star,
  GraduationCap, MessageCircle, ChevronDown,
  Shield, Clock, Target, BookOpen, FlaskConical, Calculator,
  PenLine, BarChart3, Award, Users, Globe, Play, Quote, Atom,
} from 'lucide-react';

/* ──────────────────────────────────────────────────────────────
   MOALIM — Landing page (refonte 2026)
   ─ Dark hero glassmorphism
   ─ Mock dashboard "screenshot" en JSX
   ─ 3 modes (Coaching, Libre, Examen)
   ─ Témoignages d'élèves marocains BAC
   ─ Stats, FAQ, CTA, footer
   ─ Pas de lib 3D — CSS pur + transforms
   ────────────────────────────────────────────────────────────── */

export default function Landing() {
  const { isAuthenticated } = useAuthStore();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 30);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#070718] text-white overflow-hidden relative">
      <ConcoursCalendarPopup />
      <MoalimChatbot />
      {/* Animations CSS injectées une fois */}
      <style>{`
        @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
        @keyframes float-slow { 0%,100%{transform:translateY(0) rotate(0)} 50%{transform:translateY(-20px) rotate(3deg)} }
        @keyframes pulse-glow { 0%,100%{opacity:.4} 50%{opacity:.85} }
        @keyframes shimmer { 0%{background-position:-200% 0} 100%{background-position:200% 0} }
        @keyframes fade-up {
          from { opacity: 0; transform: translateY(20px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes spin-slow { from{transform:rotate(0)} to{transform:rotate(360deg)} }
        .anim-float       { animation: float 6s ease-in-out infinite; }
        .anim-float-slow  { animation: float-slow 9s ease-in-out infinite; }
        .anim-pulse-glow  { animation: pulse-glow 4s ease-in-out infinite; }
        .anim-fade-up     { animation: fade-up .8s ease-out both; }
        .anim-spin-slow   { animation: spin-slow 30s linear infinite; }
        .gradient-text {
          background: linear-gradient(120deg,#a5b4fc 0%,#67e8f9 50%,#fbbf24 100%);
          -webkit-background-clip: text; background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .glass {
          background: rgba(255,255,255,.04);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          border: 1px solid rgba(255,255,255,.08);
        }
        .tilt-card { transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s; transform-style: preserve-3d; }
        .tilt-card:hover { transform: perspective(1000px) rotateX(-3deg) rotateY(4deg) translateY(-6px); }
        .grid-bg {
          background-image:
            linear-gradient(rgba(99,102,241,.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,102,241,.08) 1px, transparent 1px);
          background-size: 60px 60px;
        }
      `}</style>

      {/* ═══ ORBES DÉCORATIFS GLOBAUX ═══ */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[700px] h-[700px] rounded-full bg-indigo-600/20 blur-[150px] anim-pulse-glow" />
        <div className="absolute top-[40%] right-[10%] w-[500px] h-[500px] rounded-full bg-cyan-500/15 blur-[140px] anim-pulse-glow" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-0 left-[5%] w-[600px] h-[600px] rounded-full bg-fuchsia-600/10 blur-[160px] anim-pulse-glow" style={{ animationDelay: '4s' }} />
      </div>

      {/* ═══ NAV ═══ */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-[#070718]/80 backdrop-blur-2xl border-b border-white/5' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="relative">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                <span className="text-white font-bold text-sm font-brand">م</span>
              </div>
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 blur-md opacity-50 group-hover:opacity-80 transition-opacity" />
            </div>
            <div>
              <div className="font-bold text-base leading-tight">Moalim</div>
              <div className="text-[10px] text-white/40 leading-tight font-brand">معلم • IA pour le BAC</div>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-7 text-sm text-white/60">
            <a href="#features" className="hover:text-white transition">Modes</a>
            <a href="#dashboard" className="hover:text-white transition">Tableau de bord</a>
            <a href="#testimonials" className="hover:text-white transition">Témoignages</a>
            <a href="#faq" className="hover:text-white transition">FAQ</a>
          </div>

          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <Link to="/dashboard" className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-sm font-semibold hover:shadow-lg hover:shadow-indigo-500/40 transition-all">
                Mon dashboard
              </Link>
            ) : (
              <>
                <Link to="/orientation" className="hidden md:inline-flex items-center gap-1 px-3 py-2 text-sm text-amber-200 hover:text-amber-100 transition font-medium">
                  Orientation Post-BAC
                  <span className="text-[9px] bg-amber-400 text-black px-1.5 py-0.5 rounded font-bold">NEW</span>
                </Link>
                <Link to="/login" className="hidden sm:inline-block px-4 py-2 text-sm text-white/70 hover:text-white transition">
                  Connexion
                </Link>
                <Link to="/inscription" className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white text-sm font-semibold hover:shadow-lg hover:shadow-indigo-500/40 transition-all flex items-center gap-1.5">
                  Commencer
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <HeroSection />
      <TrustBar />
      <FeaturesSection />
      <DashboardPreviewSection />
      <HowItWorksSection />
      <StatsSection />
      <TestimonialsSection />
      <SubjectsSection />
      <ConcoursPrepSoonSection />
      <FAQSection />
      <FinalCTASection />
      <Footer />
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   HERO
   ════════════════════════════════════════════════════════════ */
function HeroSection() {
  return (
    <section className="relative pt-32 pb-20 sm:pt-40 sm:pb-28 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 grid lg:grid-cols-[1.05fr_1fr] gap-10 lg:gap-16 items-center">
        {/* TEXTE */}
        <div className="anim-fade-up">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass mb-6 text-xs">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
            </span>
            <span className="text-emerald-200">IA en direct • Spécial BAC Maroc 2026</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black leading-[1.05] tracking-tight mb-5">
            Le tuteur IA qui te fait
            <br />
            <span className="gradient-text">décrocher la mention</span>
          </h1>

          <p className="text-lg text-white/65 leading-relaxed max-w-xl mb-8">
            Coaching personnalisé, <b className="text-white">60 examens réels du BAC</b> corrigés instantanément, et explications au tableau interactif —
            le tout 100% aligné sur le cadre de référence officiel <b className="text-white">2ème BAC PC BIOF</b>.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 mb-8">
            <Link to="/inscription" className="group relative inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 text-white font-bold text-base shadow-2xl shadow-indigo-500/40 hover:shadow-indigo-500/60 transition-all hover:scale-[1.02]">
              <Sparkles className="w-5 h-5" />
              Démarrer gratuitement
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              <span className="absolute inset-0 rounded-2xl bg-gradient-to-r from-indigo-400 to-cyan-400 blur-xl opacity-30 group-hover:opacity-50 transition-opacity -z-10" />
            </Link>
            <a href="#features" className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl glass text-white font-semibold hover:bg-white/10 transition-all">
              <Play className="w-4 h-4" />
              Voir la démo
            </a>
          </div>

          {/* Orientation Post-BAC teaser */}
          <Link to="/orientation" className="group inline-flex items-center gap-3 px-5 py-3 mb-8 rounded-2xl bg-gradient-to-r from-amber-500/20 to-pink-500/20 border border-amber-300/30 hover:border-amber-300/60 transition-all backdrop-blur">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-400 to-pink-500 flex items-center justify-center shrink-0">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <div className="text-left">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-amber-100">Nouveau — Orientation Post-BAC</span>
                <span className="text-[9px] bg-amber-400 text-black px-1.5 py-0.5 rounded font-bold">GRATUIT</span>
              </div>
              <div className="text-xs text-white/70">Calcule tes chances aux concours ENSA, ENSAM, ENCG, ENA →</div>
            </div>
            <ArrowRight className="w-4 h-4 text-amber-200 group-hover:translate-x-1 transition-transform" />
          </Link>

          {/* Trust line */}
          <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-white/50">
            <div className="flex items-center gap-1.5">
              <div className="flex -space-x-2">
                {[
                  'from-pink-400 to-rose-500',
                  'from-blue-400 to-indigo-500',
                  'from-amber-400 to-orange-500',
                  'from-emerald-400 to-teal-500',
                ].map((g, i) => (
                  <div key={i} className={`w-7 h-7 rounded-full bg-gradient-to-br ${g} ring-2 ring-[#070718]`} />
                ))}
              </div>
              <span><b className="text-white">+1 200</b> bachelier·es</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="flex">
                {[1,2,3,4,5].map(i => (
                  <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>
              <span><b className="text-white">4.9/5</b> note moyenne</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span>Données chiffrées</span>
            </div>
          </div>
        </div>

        {/* VISUEL 3D-LIKE */}
        <div className="relative anim-fade-up" style={{ animationDelay: '.15s' }}>
          <Hero3DVisual />
        </div>
      </div>
    </section>
  );
}

/* Composition d'éléments flottants façon 3D bento */
function Hero3DVisual() {
  return (
    <div className="relative h-[480px] sm:h-[560px] grid-bg rounded-3xl overflow-hidden glass">
      {/* Halo central */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-72 h-72 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 blur-3xl opacity-40" />

      {/* Cercle anneau */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full border border-indigo-400/30 anim-spin-slow">
        <div className="absolute -top-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60" />
        <div className="absolute top-1/2 -right-1.5 -translate-y-1/2 w-2.5 h-2.5 rounded-full bg-fuchsia-400 shadow-lg shadow-fuchsia-400/60" />
        <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-amber-400 shadow-lg shadow-amber-400/60" />
      </div>

      {/* Carte centrale "AI Tutor" */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-44 h-44 rounded-3xl bg-gradient-to-br from-indigo-600 to-purple-700 shadow-2xl shadow-indigo-500/50 flex flex-col items-center justify-center anim-float">
        <div className="w-16 h-16 rounded-2xl bg-white/15 flex items-center justify-center mb-3 backdrop-blur-sm">
          <Brain className="w-9 h-9 text-white" />
        </div>
        <div className="text-white font-bold text-sm">AI Tutor</div>
        <div className="text-white/60 text-[10px] mt-1">en train de t'aider</div>
      </div>

      {/* Card haut-gauche : matière */}
      <div className="absolute top-6 left-6 glass rounded-2xl p-4 anim-float-slow w-48 shadow-xl">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center">
            <Atom className="w-4 h-4 text-indigo-300" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Physique — Ondes</div>
            <div className="text-[10px] text-white/40">2ème BAC PC BIOF</div>
          </div>
        </div>
        <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-indigo-400 to-cyan-400 rounded-full w-[78%]" />
        </div>
        <div className="text-[10px] text-indigo-200 mt-1.5 font-bold">78% maîtrisé</div>
      </div>

      {/* Card haut-droite : exam */}
      <div className="absolute top-10 right-4 glass rounded-2xl p-4 anim-float w-44 shadow-xl" style={{ animationDelay: '1s' }}>
        <div className="flex items-center gap-2 mb-2">
          <Trophy className="w-4 h-4 text-amber-400" />
          <div className="text-xs font-semibold">Examen réel BAC 2024</div>
        </div>
        <div className="text-2xl font-black gradient-text leading-none">17.5<span className="text-sm text-white/40">/20</span></div>
        <div className="text-[10px] text-white/50 mt-1">Corrigé en 0.8 s</div>
      </div>

      {/* Card bas-gauche : feedback examen */}
      <div className="absolute bottom-12 left-10 glass rounded-2xl p-3.5 anim-float-slow w-48 shadow-xl" style={{ animationDelay: '2s' }}>
        <div className="flex items-center gap-2 mb-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center">
            <Target className="w-4 h-4 text-emerald-400" />
          </div>
          <span className="text-xs font-semibold">Feedback IA</span>
        </div>
        <div className="text-[10px] text-white/70 leading-tight mb-1.5">
          "Très bien sur la cinétique. Revois les piles (ch.10)."
        </div>
        <div className="flex items-center gap-1 text-[9px] text-emerald-300">
          <Check className="w-2.5 h-2.5" /> Orientation personnalisée
        </div>
      </div>

      {/* Card bas-droite : streak */}
      <div className="absolute bottom-8 right-8 glass rounded-2xl p-4 anim-float w-36 shadow-xl" style={{ animationDelay: '1.5s' }}>
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-yellow-400" />
          <span className="text-xs font-semibold">Streak</span>
        </div>
        <div className="text-2xl font-black text-yellow-400 mt-1">12 jours</div>
        <div className="text-[10px] text-white/50">consécutifs 🔥</div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   TRUST BAR
   ════════════════════════════════════════════════════════════ */
function TrustBar() {
  const items = [
    'Lycée Lalla Aïcha',
    'Lycée Mohammed VI',
    'Lycée Al Khansaa',
    'Lycée Ibn Sina',
    'Lycée Al Farabi',
    'Lycée Hassan II',
  ];
  return (
    <section className="relative z-10 py-10 border-y border-white/5 bg-white/[.015]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <p className="text-center text-xs uppercase tracking-widest text-white/40 mb-6">
          Adopté par des élèves dans plus de 30 lycées
        </p>
        <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-4 opacity-60">
          {items.map(name => (
            <div key={name} className="flex items-center gap-2 text-white/50 text-sm font-semibold">
              <GraduationCap className="w-4 h-4" />
              {name}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   FEATURES — 3 modes
   ════════════════════════════════════════════════════════════ */
function FeaturesSection() {
  return (
    <section id="features" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="3 façons d'apprendre"
          title={<>Choisis ton <span className="gradient-text">mode</span> selon ton objectif</>}
          subtitle="Du cours guidé pas à pas à l'examen blanc chronométré, Moalim s'adapte à ton rythme."
        />

        <div className="grid md:grid-cols-3 gap-5 mt-14">
          <FeatureCard
            color="from-indigo-500 to-purple-600"
            shadow="shadow-indigo-500/30"
            icon={Brain}
            tag="Mode Coaching"
            title="Cours interactifs avec ton tuteur IA"
            desc="Le prof IA t'explique au tableau, te pose des questions, vérifie ta compréhension à chaque étape."
            features={['Tableau blanc IA', 'Voix + texte', 'Adaptation au programme officiel']}
          />
          <FeatureCard
            color="from-cyan-500 to-blue-600"
            shadow="shadow-cyan-500/30"
            icon={MessageCircle}
            tag="Mode Libre"
            title="Pose tes questions à n'importe quel moment"
            desc="Une formule à comprendre, une notion qui bloque ? Demande à l'IA, elle répond avec exemples concrets."
            features={['Réponse en français/arabe/darija', 'Schémas générés à la demande', 'Disponible 24/7']}
          />
          <FeatureCard
            color="from-amber-500 to-rose-600"
            shadow="shadow-amber-500/30"
            icon={Trophy}
            tag="Mode Examen Réel"
            title="60 examens réels du BAC corrigés en direct"
            desc="Tous les sujets nationaux récents (sessions normale + rattrapage). Correction et explication instantanée à chaque question, plus une orientation personnalisée pour cibler tes points faibles."
            features={['60 sujets BAC officiels', 'Correction + explication instantanée', 'Feedback + orientation chapitre par chapitre']}
          />
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ color, shadow, icon: Icon, tag, title, desc, features }: {
  color: string; shadow: string; icon: any; tag: string; title: string; desc: string; features: string[];
}) {
  return (
    <div className={`tilt-card relative glass rounded-3xl p-6 hover:bg-white/[.06] hover:${shadow} transition-all`}>
      <div className={`inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br ${color} mb-5 shadow-xl ${shadow}`}>
        <Icon className="w-7 h-7 text-white" />
      </div>
      <div className="text-[11px] uppercase tracking-widest text-white/40 font-semibold mb-2">{tag}</div>
      <h3 className="text-xl font-bold mb-3 text-white">{title}</h3>
      <p className="text-sm text-white/60 leading-relaxed mb-5">{desc}</p>
      <ul className="space-y-2">
        {features.map((f, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-white/70">
            <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
            {f}
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   DASHBOARD PREVIEW (mock screenshot en JSX)
   ════════════════════════════════════════════════════════════ */
function DashboardPreviewSection() {
  return (
    <section id="dashboard" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Ton tableau de bord personnel"
          title={<>Suis ta <span className="gradient-text">progression</span> en temps réel</>}
          subtitle="Chaque réponse, chaque exercice, chaque examen alimente ton bilan personnel."
        />

        {/* Mock window */}
        <div className="mt-12 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-cyan-500/20 blur-3xl opacity-50" />

          <div className="relative glass rounded-3xl overflow-hidden shadow-2xl shadow-indigo-500/30 border border-white/10">
            {/* Window chrome */}
            <div className="flex items-center justify-between px-4 py-3 bg-black/40 border-b border-white/5">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-rose-400/70" />
                <div className="w-3 h-3 rounded-full bg-amber-400/70" />
                <div className="w-3 h-3 rounded-full bg-emerald-400/70" />
              </div>
              <div className="flex items-center gap-2 px-3 py-1 rounded-md bg-white/5 text-[11px] text-white/50">
                <Globe className="w-3 h-3" />
                moalim.online/dashboard
              </div>
              <div className="w-12" />
            </div>

            <DashboardMock />
          </div>
        </div>
      </div>
    </section>
  );
}

function DashboardMock() {
  return (
    <div className="bg-[#0b0b1d] p-4 sm:p-6 grid lg:grid-cols-[260px_1fr] gap-4 min-h-[560px]">
      {/* Sidebar mock */}
      <aside className="hidden lg:flex flex-col gap-1 p-3 rounded-2xl bg-white/[.02] border border-white/5">
        <div className="flex items-center gap-2 p-3 mb-2">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center font-brand font-bold">م</div>
          <div>
            <div className="text-sm font-bold">Moalim</div>
            <div className="text-[10px] text-white/40">Bonjour, Yasmine</div>
          </div>
        </div>
        {[
          { icon: BarChart3, label: 'Tableau de bord', active: true },
          { icon: Brain, label: 'Coaching IA' },
          { icon: MessageCircle, label: 'Mode libre' },
          { icon: Trophy, label: 'Examens réels' },
          { icon: BookOpen, label: 'Mes cours' },
          { icon: Award, label: 'Progression' },
        ].map((it, i) => (
          <div key={i} className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm cursor-default ${
            it.active ? 'bg-indigo-500/15 text-indigo-200' : 'text-white/50'
          }`}>
            <it.icon className="w-4 h-4" />
            {it.label}
          </div>
        ))}
      </aside>

      {/* Main mock */}
      <main className="space-y-4">
        {/* Greeting */}
        <div className="rounded-2xl p-5 bg-gradient-to-br from-indigo-600/30 via-purple-600/20 to-cyan-600/20 border border-white/5 relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-40 h-40 rounded-full bg-cyan-400/20 blur-3xl" />
          <div className="relative flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 className="text-lg sm:text-xl font-bold mb-1">Bon retour, Yasmine ✨</h3>
              <p className="text-sm text-white/60">Tu as <b className="text-white">3 nouveaux exercices</b> recommandés en SVT</p>
            </div>
            <button className="px-4 py-2 rounded-xl bg-white/10 text-sm font-semibold flex items-center gap-2 cursor-default">
              Continuer ma session <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: 'Heures', value: '47h', delta: '+5h', color: 'from-indigo-500 to-blue-600', icon: Clock },
            { label: 'Exercices', value: '128', delta: '+12', color: 'from-emerald-500 to-teal-600', icon: PenLine },
            { label: 'Score moy.', value: '15.8/20', delta: '+1.4', color: 'from-amber-500 to-orange-600', icon: Trophy },
            { label: 'Streak', value: '12j', delta: '🔥', color: 'from-rose-500 to-pink-600', icon: Zap },
          ].map((k, i) => (
            <div key={i} className="glass rounded-2xl p-4">
              <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${k.color} flex items-center justify-center mb-2`}>
                <k.icon className="w-4 h-4 text-white" />
              </div>
              <div className="text-[11px] text-white/50 font-medium">{k.label}</div>
              <div className="flex items-baseline gap-1.5">
                <span className="text-xl font-black text-white">{k.value}</span>
                <span className="text-[10px] text-emerald-400 font-bold">{k.delta}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Charts row */}
        <div className="grid lg:grid-cols-[1.3fr_1fr] gap-3">
          {/* Bar chart */}
          <div className="glass rounded-2xl p-4">
            <div className="flex items-center justify-between mb-3">
              <div>
                <div className="text-sm font-semibold">Progression hebdo</div>
                <div className="text-[11px] text-white/40">Heures par matière</div>
              </div>
              <div className="text-[10px] text-white/40">Avr 25 — Mai 1</div>
            </div>
            <div className="flex items-end gap-2 h-32">
              {[
                { d: 'L', svt: 60, pc: 40, math: 30 },
                { d: 'M', svt: 45, pc: 70, math: 50 },
                { d: 'M', svt: 80, pc: 55, math: 60 },
                { d: 'J', svt: 50, pc: 85, math: 40 },
                { d: 'V', svt: 65, pc: 60, math: 75 },
                { d: 'S', svt: 90, pc: 70, math: 85 },
                { d: 'D', svt: 75, pc: 50, math: 60 },
              ].map((day, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-1">
                  <div className="w-full flex flex-col gap-0.5 h-full justify-end">
                    <div className="rounded-t-sm bg-gradient-to-t from-emerald-400 to-emerald-300" style={{ height: `${day.svt}%` }} />
                    <div className="rounded-t-sm bg-gradient-to-t from-indigo-400 to-indigo-300" style={{ height: `${day.pc}%` }} />
                    <div className="rounded-t-sm bg-gradient-to-t from-amber-400 to-amber-300" style={{ height: `${day.math}%` }} />
                  </div>
                  <div className="text-[10px] text-white/40">{day.d}</div>
                </div>
              ))}
            </div>
            <div className="flex gap-3 mt-3 text-[10px] text-white/50">
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-emerald-400" />SVT</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-indigo-400" />PC</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm bg-amber-400" />Math</span>
            </div>
          </div>

          {/* Mention projetée */}
          <div className="glass rounded-2xl p-4 flex flex-col">
            <div className="text-sm font-semibold mb-1">Mention projetée</div>
            <div className="text-[11px] text-white/40 mb-3">Sur la base de tes 6 dernières évaluations</div>

            <div className="flex-1 flex items-center justify-center relative">
              <svg className="w-32 h-32 -rotate-90">
                <circle cx="64" cy="64" r="52" stroke="rgba(255,255,255,.08)" strokeWidth="10" fill="none" />
                <circle cx="64" cy="64" r="52" stroke="url(#grad1)" strokeWidth="10" fill="none"
                  strokeDasharray="326" strokeDashoffset="98" strokeLinecap="round" />
                <defs>
                  <linearGradient id="grad1" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0" stopColor="#6366f1" />
                    <stop offset="1" stopColor="#22d3ee" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-3xl font-black gradient-text leading-none">15.8</div>
                <div className="text-[10px] text-white/50 mt-1">/ 20</div>
              </div>
            </div>
            <div className="text-center mt-3">
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-300 text-[11px] font-bold">
                🏆 Mention Très Bien
              </span>
            </div>
          </div>
        </div>

        {/* Recent sessions */}
        <div className="glass rounded-2xl p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="text-sm font-semibold">Sessions récentes</div>
            <div className="text-[10px] text-white/40">Voir tout</div>
          </div>
          <div className="space-y-2">
            {[
              { mode: 'Coaching', subj: 'Dipole RC — charge et décharge', time: 'Il y a 2h', score: '92%', color: 'indigo' },
              { mode: 'Examen', subj: 'PC — Sujet BAC 2024 (normale)', time: 'Hier', score: '17/20', color: 'amber' },
              { mode: 'Libre', subj: 'Cinétique : facteurs et catalyse', time: 'Il y a 2 j', score: '—', color: 'cyan' },
            ].map((s, i) => (
              <div key={i} className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/[.03] hover:bg-white/[.06] transition-colors">
                <div className={`w-9 h-9 rounded-xl bg-${s.color}-500/15 flex items-center justify-center text-${s.color}-300 text-[10px] font-bold`}>
                  {s.mode.slice(0, 2).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold truncate">{s.subj}</div>
                  <div className="text-[11px] text-white/40">{s.mode} · {s.time}</div>
                </div>
                <div className="text-sm font-bold text-emerald-300">{s.score}</div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   HOW IT WORKS
   ════════════════════════════════════════════════════════════ */
function HowItWorksSection() {
  const steps = [
    { n: '01', icon: GraduationCap, title: 'Crée ton compte', desc: 'Inscription en 30 secondes, sélectionne tes matières BAC.' },
    { n: '02', icon: Target, title: 'Diagnostic initial', desc: "L'IA évalue ton niveau pour adapter le contenu à ton rythme." },
    { n: '03', icon: Brain, title: 'Sessions guidées', desc: 'Le tuteur t\'explique au tableau et te corrige en direct.' },
    { n: '04', icon: Trophy, title: 'Examens blancs', desc: 'Teste-toi sur les sujets nationaux et obtiens ta mention.' },
  ];
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Comment ça marche"
          title={<>De zéro à <span className="gradient-text">mention</span> en 4 étapes</>}
        />

        <div className="grid md:grid-cols-4 gap-4 mt-12 relative">
          {/* Connector line */}
          <div className="hidden md:block absolute top-16 left-[12.5%] right-[12.5%] h-px bg-gradient-to-r from-transparent via-indigo-400/40 to-transparent" />

          {steps.map((s, i) => (
            <div key={i} className="relative tilt-card glass rounded-2xl p-5 text-center">
              <div className="w-14 h-14 rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 mx-auto mb-4 flex items-center justify-center shadow-lg shadow-indigo-500/40 relative z-10">
                <s.icon className="w-6 h-6 text-white" />
              </div>
              <div className="text-[10px] tracking-widest text-indigo-300 font-bold mb-1">ÉTAPE {s.n}</div>
              <h3 className="text-base font-bold mb-2">{s.title}</h3>
              <p className="text-xs text-white/55 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   STATS
   ════════════════════════════════════════════════════════════ */
function StatsSection() {
  const stats = [
    { v: '+1 200', l: 'élèves actif·ves', sub: 'partout au Maroc' },
    { v: '94%', l: 'élèves satisfait·es', sub: 'note 4 ou 5/5' },
    { v: '+2.3', l: 'points en moyenne', sub: 'gagnés en 6 semaines' },
    { v: '24/7', l: 'disponibilité', sub: 'IA toujours dispo' },
  ];
  return (
    <section className="relative z-10 py-16 sm:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="rounded-3xl glass p-8 sm:p-12 relative overflow-hidden">
          <div className="absolute -top-20 -left-20 w-72 h-72 rounded-full bg-indigo-500/20 blur-3xl" />
          <div className="absolute -bottom-20 -right-20 w-72 h-72 rounded-full bg-cyan-500/20 blur-3xl" />
          <div className="relative grid sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 text-center">
            {stats.map((s, i) => (
              <div key={i}>
                <div className="text-4xl sm:text-5xl font-black gradient-text leading-none">{s.v}</div>
                <div className="text-sm font-semibold text-white mt-2">{s.l}</div>
                <div className="text-[11px] text-white/40 mt-1">{s.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   TESTIMONIALS
   ════════════════════════════════════════════════════════════ */
function TestimonialsSection() {
  const items = [
    {
      name: 'Yasmine B.', school: 'Lycée Lalla Aïcha — Casablanca', subject: '2BAC PC BIOF',
      score: 'Physique 17.8/20', avatar: 'from-pink-400 to-rose-500',
      quote: "J'avais peur des dipôles RLC mais le coaching IA explique au tableau étape par étape. En 2 mois j'ai gagné 3 points en physique.",
    },
    {
      name: 'Mehdi A.', school: 'Lycée Mohammed VI — Rabat', subject: '2BAC PC BIOF',
      score: 'Chimie 18.2/20', avatar: 'from-blue-400 to-indigo-500',
      quote: "Les 60 examens réels avec correction instantanée, c'est dingue. Tu finis ta copie, tu reçois ta note + les commentaires question par question. Ça m'a sauvé pour le BAC.",
    },
    {
      name: 'Salma K.', school: 'Lycée Al Khansaa — Fès', subject: '2BAC PC BIOF',
      score: 'Maths 16.5/20', avatar: 'from-amber-400 to-orange-500',
      quote: "Je peux poser n'importe quelle question, même en darija, et l'IA répond avec des schémas. C'est comme avoir un prof particulier disponible 24h/24.",
    },
    {
      name: 'Anas E.', school: 'Lycée Ibn Sina — Marrakech', subject: '2BAC PC BIOF',
      score: 'Moyenne 15.9/20', avatar: 'from-emerald-400 to-teal-500',
      quote: "L'orientation après chaque examen me dit exactement quel chapitre revoir. J'ai arrêté de réviser dans le vide, je cible mes points faibles.",
    },
    {
      name: 'Nada R.', school: 'Lycée Al Farabi — Tanger', subject: '2BAC PC BIOF',
      score: 'Physique 17.1/20', avatar: 'from-fuchsia-400 to-purple-500',
      quote: "Les explications sur les ondes lumineuses sont claires, avec des schémas dessinés en direct sur le tableau. Même la diffraction devient évidente.",
    },
    {
      name: 'Hamza T.', school: 'Lycée Hassan II — Agadir', subject: '2BAC PC BIOF',
      score: 'Maths 18.5/20', avatar: 'from-cyan-400 to-blue-500',
      quote: "L'IA me fait travailler les démos étape par étape. Quand je bloque, elle reformule et donne des indices, jamais la réponse directe. Pédagogiquement c'est parfait.",
    },
  ];

  return (
    <section id="testimonials" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Témoignages"
          title={<>Ce que disent les <span className="gradient-text">bachelier·es</span></>}
          subtitle="Des élèves de toutes les villes du Maroc utilisent Moalim chaque jour."
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-14">
          {items.map((t, i) => (
            <div key={i} className="tilt-card glass rounded-2xl p-6 hover:bg-white/[.06] transition-all relative">
              <Quote className="absolute top-4 right-4 w-6 h-6 text-white/10" />

              {/* Stars */}
              <div className="flex gap-0.5 mb-4">
                {[1,2,3,4,5].map(s => (
                  <Star key={s} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>

              <p className="text-sm text-white/75 leading-relaxed mb-5 italic">"{t.quote}"</p>

              <div className="flex items-center gap-3 pt-4 border-t border-white/5">
                <div className={`w-11 h-11 rounded-full bg-gradient-to-br ${t.avatar} flex items-center justify-center font-bold text-white shadow-lg`}>
                  {t.name.charAt(0)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-white truncate">{t.name}</div>
                  <div className="text-[11px] text-white/45 truncate">{t.school}</div>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-white/60">{t.subject}</span>
                    <span className="text-[10px] font-bold text-emerald-400">→ {t.score}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   SUBJECTS
   ════════════════════════════════════════════════════════════ */
function SubjectsSection() {
  const subjects = [
    {
      name: 'Physique', icon: Atom,
      color: 'from-indigo-500 to-blue-600',
      count: 15,
      topics: [
        'Ondes mécaniques progressives',
        'Ondes lumineuses (diffraction, interférences)',
        'Dipôles RC, RL et circuit RLC',
        'Modulation d’amplitude',
        'Lois de Newton & chute libre',
        'Mouvements plans · satellites · rotation',
        'Oscillateurs mécaniques',
        'Atome et mécanique de Newton',
      ],
    },
    {
      name: 'Chimie', icon: FlaskConical,
      color: 'from-rose-500 to-pink-600',
      count: 14,
      topics: [
        'Transformations lentes / rapides',
        'Vitesse de réaction · catalyse',
        'Décroissance radioactive',
        'Noyaux, masse et énergie',
        'Transformations dans les 2 sens · équilibre',
        'Réactions acide-base · pH · pKa',
        'Dosage acido-basique',
        'Piles · électrolyse · estérification',
      ],
    },
    {
      name: 'Mathématiques', icon: Calculator,
      color: 'from-amber-500 to-orange-600',
      count: 10,
      topics: [
        'Limites · continuité · dérivation',
        'Fonctions logarithme & exponentielle',
        'Calcul intégral',
        'Équations différentielles',
        'Suites numériques · récurrence',
        'Nombres complexes',
        'Probabilités',
        'Géométrie dans l’espace',
      ],
    },
  ];
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Cadre de référence officiel"
          title={<>Tout le programme <span className="gradient-text">2ème BAC PC BIOF</span></>}
          subtitle="Chapitres et leçons issus directement du référentiel du Ministère de l’Éducation Nationale (BIOF). Aucune matière hors-programme."
        />
        <div className="grid md:grid-cols-3 gap-5 mt-12">
          {subjects.map((s, i) => (
            <div key={i} className="tilt-card glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.color} flex items-center justify-center shadow-lg`}>
                    <s.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-base font-bold">{s.name}</div>
                    <div className="text-[11px] text-white/40">2ème BAC PC BIOF</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-black gradient-text leading-none">{s.count}</div>
                  <div className="text-[10px] text-white/40 mt-0.5">chapitres</div>
                </div>
              </div>
              <ul className="space-y-1.5">
                {s.topics.map((t, j) => (
                  <li key={j} className="flex items-start gap-1.5 text-[12px] text-white/70 leading-tight">
                    <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
              <div className="text-[11px] text-white/40 mt-4 pt-3 border-t border-white/5">+ tous les chapitres restants du référentiel</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   CONCOURS PREP — BIENTÔT (Phase 2, marketing teaser)
   ════════════════════════════════════════════════════════════ */
function ConcoursPrepSoonSection() {
  const concours = [
    { name: 'ENSA', desc: 'Écoles Nationales des Sciences Appliquées', color: 'from-blue-500 to-indigo-600', icon: '⚙️', places: '2 800 places' },
    { name: 'ENSAM', desc: "Arts et Métiers — Ingénierie d'excellence", color: 'from-violet-500 to-purple-600', icon: '🔧', places: '450 places' },
    { name: 'ENCG · TAFEM', desc: 'Écoles Nationales de Commerce', color: 'from-emerald-500 to-teal-600', icon: '📊', places: '2 200 places' },
    { name: 'Médecine · FMP', desc: 'Concours des Facultés de Médecine', color: 'from-rose-500 to-pink-600', icon: '⚕️', places: '3 400 places' },
    { name: 'Architecture', desc: 'ENA Rabat / Tétouan / Marrakech', color: 'from-amber-500 to-orange-600', icon: '🏛️', places: '180 places' },
    { name: 'CPGE', desc: 'Classes Préparatoires aux Grandes Écoles', color: 'from-cyan-500 to-sky-600', icon: '🎯', places: '3 200 places' },
  ];

  const features = [
    { icon: BookOpen,  title: 'Annales officielles',     desc: '15 ans de sujets par concours, corrigés & commentés par l\'IA.' },
    { icon: Target,    title: 'QCM adaptatifs',          desc: "L'IA détecte tes lacunes et cible les questions-clés de chaque concours." },
    { icon: Clock,     title: 'Simulations chronométrées', desc: 'Entraînement en conditions réelles, format exact du jour J.' },
    { icon: Brain,     title: 'Coaching stratégique',     desc: 'Plan de préparation personnalisé selon ton Bac et ton concours cible.' },
  ];

  return (
    <section className="relative z-10 py-20 sm:py-28">
      {/* Background glow */}
      <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-[500px] bg-gradient-to-r from-amber-500/10 via-pink-500/10 to-indigo-500/10 blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-amber-500/20 to-pink-500/20 border border-amber-300/30 mb-5">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-400" />
            </span>
            <span className="text-xs uppercase tracking-widest font-bold text-amber-200">Phase 2 · Bientôt</span>
            <span className="text-[10px] bg-amber-400 text-black px-1.5 py-0.5 rounded font-black">2026</span>
          </div>

          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black leading-[1.05] tracking-tight mb-5">
            On ne s'arrête pas au <span className="gradient-text">BAC</span>.
            <br />
            <span className="text-white/90 text-3xl sm:text-4xl lg:text-5xl">La prépa concours arrive.</span>
          </h2>

          <p className="text-lg text-white/65 leading-relaxed max-w-2xl mx-auto">
            <b className="text-white">Décrocher la mention ne suffit plus.</b> Il faut préparer les concours des grandes écoles marocaines pour
            sécuriser sa place. Moalim étend son IA à la <span className="text-amber-200 font-semibold">préparation post-BAC complète</span> —
            de l'oral de TAFEM aux épreuves de maths de l'ENSA.
          </p>
        </div>

        {/* Concours grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4 mb-12">
          {concours.map((c) => (
            <div
              key={c.name}
              className="group relative p-4 sm:p-5 rounded-2xl glass border border-white/5 hover:border-white/15 transition-all hover:-translate-y-1"
            >
              {/* Glow on hover */}
              <div className={`absolute -inset-px rounded-2xl bg-gradient-to-br ${c.color} opacity-0 group-hover:opacity-20 transition-opacity pointer-events-none blur-sm`} />

              <div className="relative">
                <div className={`w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-br ${c.color} flex items-center justify-center text-xl sm:text-2xl mb-3 shadow-lg`}>
                  {c.icon}
                </div>
                <div className="flex items-start justify-between gap-2 mb-1">
                  <h3 className="font-black text-white text-sm sm:text-base leading-tight">{c.name}</h3>
                  <span className="text-[9px] sm:text-[10px] bg-white/10 text-white/70 px-1.5 py-0.5 rounded font-bold whitespace-nowrap">
                    {c.places}
                  </span>
                </div>
                <p className="text-xs text-white/55 leading-snug">{c.desc}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Features bento */}
        <div className="rounded-3xl glass p-6 sm:p-10 border border-white/10 relative overflow-hidden">
          <div className="absolute -top-24 -right-24 w-64 h-64 rounded-full bg-amber-500/15 blur-3xl" />
          <div className="absolute -bottom-24 -left-24 w-72 h-72 rounded-full bg-pink-500/15 blur-3xl" />

          <div className="relative grid lg:grid-cols-[1fr_1.3fr] gap-8 lg:gap-12 items-center">
            {/* LEFT — Pitch */}
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-[11px] font-bold text-indigo-200 uppercase tracking-widest mb-4">
                <Trophy className="w-3 h-3" />
                Avantage stratégique
              </div>
              <h3 className="text-2xl sm:text-3xl font-black text-white leading-tight mb-4">
                Une seule plateforme, du lycée à <span className="gradient-text">la grande école</span>.
              </h3>
              <p className="text-sm sm:text-base text-white/65 leading-relaxed mb-6">
                Pendant que tes camarades cherchent un nouveau prof particulier pour chaque concours,
                <b className="text-white"> toi, tu restes sur Moalim.</b> L'IA connaît déjà ton profil,
                tes lacunes, tes forces — elle ajuste la préparation concours en continuité avec ton parcours BAC.
              </p>

              {/* Benefits */}
              <ul className="space-y-2.5 mb-6">
                {[
                  'Continuité pédagogique : 0 effort de re-paramétrage',
                  '1 abonnement au lieu de 5 profs particuliers',
                  'Données des 15 dernières années par concours',
                  'IA qui apprend de toi, pas l\'inverse',
                ].map((b) => (
                  <li key={b} className="flex items-start gap-2 text-sm text-white/75">
                    <Check className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                    <span>{b}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <Link
                to="/inscription"
                className="group inline-flex items-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-amber-500 via-pink-500 to-indigo-500 text-white font-bold text-sm shadow-xl shadow-pink-500/30 hover:shadow-pink-500/50 hover:scale-[1.02] transition-all"
              >
                <Sparkles className="w-4 h-4" />
                Accès prioritaire gratuit
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <p className="text-[11px] text-white/40 mt-2">
                Inscris-toi maintenant → accès <b className="text-amber-200">gratuit à vie</b> aux modules concours dès leur lancement.
              </p>
            </div>

            {/* RIGHT — Features grid */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4">
              {features.map((f) => (
                <div
                  key={f.title}
                  className="p-4 sm:p-5 rounded-2xl bg-white/[0.03] border border-white/5 hover:border-indigo-400/30 transition-colors"
                >
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-400/20 flex items-center justify-center mb-3">
                    <f.icon className="w-4 h-4 text-indigo-300" />
                  </div>
                  <h4 className="font-bold text-white text-sm mb-1">{f.title}</h4>
                  <p className="text-xs text-white/50 leading-snug">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Roadmap ribbon */}
        <div className="mt-8 flex items-center justify-center gap-4 sm:gap-8 text-xs text-white/40 flex-wrap">
          <div className="flex items-center gap-1.5">
            <Check className="w-3.5 h-3.5 text-emerald-400" />
            <span><b className="text-white/80">Aujourd'hui</b> · BAC complet</span>
          </div>
          <span className="text-white/20">→</span>
          <div className="flex items-center gap-1.5">
            <div className="w-3.5 h-3.5 rounded-full border-2 border-amber-400 border-t-transparent animate-spin" />
            <span><b className="text-amber-200">Phase 2</b> · Concours grandes écoles</span>
          </div>
          <span className="text-white/20">→</span>
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-white/30" />
            <span><b className="text-white/60">Après</b> · Prépa études supérieures</span>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   FAQ
   ════════════════════════════════════════════════════════════ */
function FAQSection() {
  const faqs = [
    { q: "Est-ce vraiment gratuit pour commencer ?", a: "Oui. Tu peux créer un compte, faire des sessions de coaching et passer un examen réel sans aucune carte bancaire. Une fois que tu vois la valeur, tu peux passer au plan complet." },
    { q: "Quelle filière est couverte ?", a: "Pour le moment, Moalim couvre exclusivement la 2ème année du Baccalauréat Sciences PC BIOF (Sciences Physiques et Chimiques, programme international francophone). Les chapitres de Physique, Chimie et Mathématiques sont issus directement du cadre de référence officiel du Ministère de l'Éducation Nationale." },
    { q: "Combien d'examens BAC sont disponibles ?", a: "60 sujets réels du BAC national — sessions normale + rattrapage des dernières années. Chaque copie est corrigée et expliquée instantanément par l'IA, avec un feedback question par question et une orientation chapitre par chapitre." },
    { q: "L'IA parle-t-elle en arabe ou en darija ?", a: "Oui, tu choisis : Français, Arabe classique, ou Darija marocaine. Tu peux mélanger les langues pendant la session et l'IA s'adapte." },
    { q: "Puis-je l'utiliser sur mon téléphone ?", a: "Oui. Moalim fonctionne sur ordinateur, tablette et téléphone — sans rien à installer. Une simple connexion internet suffit." },
    { q: "Combien de temps pour voir des résultats ?", a: "En moyenne, nos élèves gagnent +2,3 points de moyenne en 6 semaines à raison de 3 sessions par semaine. Tout dépend de ton point de départ." },
    { q: "Mes données sont-elles en sécurité ?", a: "Toutes les données sont chiffrées en transit (HTTPS) et au repos. Nous ne partageons jamais tes informations avec des tiers." },
  ];
  const [open, setOpen] = useState<number | null>(0);
  return (
    <section id="faq" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="FAQ"
          title={<>Tu as une <span className="gradient-text">question</span> ?</>}
        />
        <div className="space-y-3 mt-12">
          {faqs.map((f, i) => (
            <div key={i} className="glass rounded-2xl overflow-hidden">
              <button onClick={() => setOpen(open === i ? null : i)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-white/[.03] transition-colors">
                <span className="font-semibold text-sm sm:text-base pr-4">{f.q}</span>
                <ChevronDown className={`w-5 h-5 text-white/50 flex-shrink-0 transition-transform ${open === i ? 'rotate-180' : ''}`} />
              </button>
              <div className={`overflow-hidden transition-all duration-300 ${open === i ? 'max-h-48' : 'max-h-0'}`}>
                <div className="px-5 pb-5 text-sm text-white/65 leading-relaxed">{f.a}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   FINAL CTA
   ════════════════════════════════════════════════════════════ */
function FinalCTASection() {
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        <div className="relative rounded-3xl overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-cyan-500" />
          <div className="absolute inset-0 grid-bg opacity-20" />
          <div className="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-white/20 blur-3xl" />

          <div className="relative p-8 sm:p-14 text-center text-white">
            <Sparkles className="w-10 h-10 mx-auto mb-5 anim-float" />
            <h2 className="text-3xl sm:text-5xl font-black mb-4 leading-tight">
              Prêt à décrocher ta mention ?
            </h2>
            <p className="text-base sm:text-lg text-white/85 max-w-xl mx-auto mb-8">
              Rejoins les +1 200 bachelier·es qui révisent intelligemment avec Moalim.
              Inscription gratuite, aucune carte requise.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link to="/inscription" className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-2xl bg-white text-indigo-700 font-bold shadow-2xl hover:scale-105 transition-transform">
                <GraduationCap className="w-5 h-5" />
                Créer mon compte
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link to="/login" className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-2xl bg-white/10 backdrop-blur text-white font-semibold border border-white/30 hover:bg-white/20 transition-all">
                J'ai déjà un compte
              </Link>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 mt-8 text-xs text-white/75">
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5" /> Sans carte bancaire</span>
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5" /> Annulation libre</span>
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5" /> Données chiffrées</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════════════════════════ */
function Footer() {
  return (
    <footer className="relative z-10 border-t border-white/5 py-12 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center font-brand font-bold">م</div>
              <div className="font-bold">Moalim</div>
            </div>
            <p className="text-xs text-white/50 leading-relaxed max-w-xs">
              Le tuteur IA des bachelier·es marocain·es. Spécial 2ème BAC Sciences.
            </p>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Produit</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><a href="#features" className="hover:text-white">Modes</a></li>
              <li><a href="#dashboard" className="hover:text-white">Tableau de bord</a></li>
              <li><Link to="/inscription" className="hover:text-white">Inscription</Link></li>
            </ul>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Aide</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><a href="#faq" className="hover:text-white">FAQ</a></li>
              <li><a href="mailto:contact@moalim.online" className="hover:text-white">Contact</a></li>
              <li><Link to="/login" className="hover:text-white">Connexion</Link></li>
            </ul>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Légal</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><span>Mentions légales</span></li>
              <li><span>Politique de confidentialité</span></li>
              <li><span>CGU</span></li>
            </ul>
          </div>
        </div>
        <div className="pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/40">
          <span>© 2026 Moalim · معلم — Fait avec ❤️ au Maroc 🇲🇦</span>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1"><Users className="w-3.5 h-3.5" /> +1 200 élèves</span>
            <span className="flex items-center gap-1"><Globe className="w-3.5 h-3.5" /> moalim.online</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

/* ════════════════════════════════════════════════════════════
   SECTION HEADER
   ════════════════════════════════════════════════════════════ */
function SectionHeader({ eyebrow, title, subtitle }: { eyebrow: string; title: React.ReactNode; subtitle?: string; }) {
  return (
    <div className="text-center max-w-2xl mx-auto">
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass text-xs uppercase tracking-widest text-indigo-200 font-bold mb-4">
        {eyebrow}
      </div>
      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight mb-3">{title}</h2>
      {subtitle && <p className="text-base text-white/55 leading-relaxed">{subtitle}</p>}
    </div>
  );
}
