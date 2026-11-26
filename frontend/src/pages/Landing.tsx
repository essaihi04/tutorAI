import { lazy, Suspense, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import ConcoursCalendarPopup from '../components/ConcoursCalendarPopup';
import MoalimChatbot from '../components/MoalimChatbot';
import TableauVivant, { CadreAnimation, useVisible, type Extrait } from '../components/landing/TableauVivant';
import extraits from '../components/landing/extraits.json';

/** Le survol 3D (three.js) ouvre la page ; il est chargé à part pour ne pas alourdir le reste. */
const VolDesMatieres = lazy(() => import('../components/landing/VolDesMatieres'));
import { ANNEE_SCOLAIRE, BAC_YEAR, joursAvantBac } from '../config/bac';
import {
  Brain, Trophy, ArrowRight, Check, Star, GraduationCap, MessageCircle, ChevronDown, Zap,
  Clock, Target, BookOpen, FlaskConical, Calculator, PenLine, BarChart3, Award, Users, Globe,
  Quote, Atom, Flame, School, Leaf, Sprout, HeartHandshake, Mic, Pencil, NotebookPen, Sigma, TrendingUp, Bell, Compass,
} from 'lucide-react';

/* ──────────────────────────────────────────────────────────────
   MOALIM — Landing page (refonte du 26 novembre 2026)

   Charte « tableau noir » : la vitrine a la même identité que le produit.
   ─ Fond : l'ardoise verte des cours (#0a1410 → #0f1d18), quadrillée.
   ─ Craie : titres jaunes, résultats verts, pièges et urgences roses, liens cyan
     (même code que docs/lexique-visuel/craie.md).
   ─ Écriture : Patrick Hand (la craie des cours) pour les accents, Inter pour lire.
   ─ Matières : Maths jaune · Physique cyan · Chimie orange · SVT vert.
   ─ Cartes : un trait de craie, coins irréguliers ; plus de verre dépoli violet.
   Le hero montre le produit lui-même : les animations des cours, en direct,
   et le tuteur 3D de la séance.
   ────────────────────────────────────────────────────────────── */

const MATIERE = { maths: '#facc15', physique: '#22d3ee', chimie: '#fb923c', svt: '#4ade80' } as const;
const SIM = '/media/simulations';

/** Les extraits du hero : de vraies diapositives des cours (scripts/extraits_landing.py). */
const EXTRAITS = extraits as Extrait[];
const COULEURS: Record<string, string> = { ...MATIERE, national: '#f472b6' };

export default function Landing() {
  const { isAuthenticated } = useAuthStore();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 30);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <div className="lp min-h-screen text-slate-200 overflow-x-clip relative">
      <ConcoursCalendarPopup autoOpen={false} />
      <MoalimChatbot />
      <style>{`
        .lp {
          --ardoise: #0a1410; --ardoise-2: #0f1d18; --craie: #e2e8f0;
          --jaune: #facc15; --vert: #4ade80; --rose: #f472b6; --cyan: #22d3ee; --orange: #fb923c;
          background:
            linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px) 0 0 / 28px 28px,
            linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px) 0 0 / 28px 28px,
            radial-gradient(ellipse 120% 60% at 50% 0%, #16302a 0, var(--ardoise-2) 45%, var(--ardoise) 100%);
          background-color: var(--ardoise);
        }
        .lp .craie { font-family: 'Patrick Hand','Caveat','Segoe Print','Bradley Hand','Comic Sans MS',cursive; font-weight: 400; letter-spacing: .01em; }
        .lp-carte {
          background: rgba(226,232,240,.035);
          border: 1.5px solid rgba(226,232,240,.16);
          border-radius: 20px 15px 19px 14px / 14px 19px 15px 20px;
          transition: transform .3s cubic-bezier(.2,.8,.2,1), border-color .3s, background .3s;
        }
        .lp-carte:hover { border-color: rgba(226,232,240,.34); background: rgba(226,232,240,.055); }
        .lp-leve:hover { transform: translateY(-5px) rotate(-.3deg); }
        .lp-btn {
          display: inline-flex; align-items: center; justify-content: center; gap: .5rem;
          background: var(--jaune); color: #14110a; font-weight: 800;
          border-radius: 16px 12px 15px 11px / 11px 15px 12px 16px;
          box-shadow: 0 6px 0 #a16207, 0 14px 30px -8px rgba(250,204,21,.45);
          transition: transform .15s, box-shadow .15s;
        }
        .lp-btn:hover { transform: translateY(2px); box-shadow: 0 4px 0 #a16207, 0 10px 24px -8px rgba(250,204,21,.55); }
        .lp-btn:active { transform: translateY(6px); box-shadow: 0 0 0 #a16207; }
        .lp-btn-2 {
          display: inline-flex; align-items: center; justify-content: center; gap: .5rem;
          border: 1.5px dashed rgba(226,232,240,.4); color: var(--craie); font-weight: 600;
          border-radius: 16px 12px 15px 11px / 11px 15px 12px 16px; transition: border-color .2s, background .2s;
        }
        .lp-btn-2:hover { border-color: var(--craie); background: rgba(226,232,240,.06); }
        /* Un mot souligné à la craie : le trait se dessine */
        .lp-trait { position: relative; white-space: nowrap; }
        .lp-trait::after {
          content: ''; position: absolute; left: -2%; right: -2%; bottom: -.12em; height: .32em;
          background: no-repeat center / 100% 100% url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 12' preserveAspectRatio='none'%3E%3Cpath d='M2 8 C 40 2, 70 11, 110 6 S 170 3, 198 7' fill='none' stroke='%23facc15' stroke-width='3.5' stroke-linecap='round'/%3E%3C/svg%3E");
          clip-path: inset(0 100% 0 0); animation: lp-tracer 1.1s .5s cubic-bezier(.6,.1,.3,1) forwards;
        }
        @keyframes lp-tracer { to { clip-path: inset(0 0 0 0); } }
        /* Les mots clés de la promesse en darija : ils prennent leur couleur l'un après l'autre et un trait de craie
           se dessine dessous, de droite à gauche (sens de l'écriture arabe) */
        .lp-mot { position: relative; color: #fff; transition: color .6s ease, text-shadow .6s ease; }
        .lp-mot::after {
          content: ''; position: absolute; right: -1%; left: -1%; bottom: .02em; height: .11em; border-radius: 99px;
          background: currentColor; opacity: .85; clip-path: inset(0 0 0 100%);
        }
        .lp-mots-vus .lp-mot { color: var(--mot); text-shadow: 0 0 18px color-mix(in srgb, var(--mot) 45%, transparent); transition-delay: var(--attente); }
        .lp-mots-vus .lp-mot::after { animation: lp-tracer .9s cubic-bezier(.6,.1,.3,1) forwards; animation-delay: calc(var(--attente) + .25s); }
        @keyframes lp-monte { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
        .lp-monte { animation: lp-monte .7s ease-out both; }
        @keyframes lp-ecoule { from { width: 0; } to { width: 100%; } }
        .lp-ecoule { animation: lp-ecoule linear both; }
        @keyframes lp-defile { to { transform: translateX(-50%); } }
        .lp-defile { animation: lp-defile 38s linear infinite; }
        @keyframes lp-onde { to { stroke-dashoffset: -48; } }
        @keyframes lp-barres { 0%,100% { transform: scaleY(.35); } 50% { transform: scaleY(1); } }
        @keyframes lp-pulse { 0%,100% { opacity: .35; } 50% { opacity: 1; } }

        /* Le tuteur à côté du tableau */
        .lp-tuteur { left: 0; bottom: -166px; width: 180px; transform: scale(.72); transform-origin: 0 100%; z-index: 5; }
        .lp-bulle {
          position: absolute; left: 172px; top: 96px; width: max-content; max-width: 270px;
          padding: .5rem .8rem; font-size: 1.2rem; line-height: 1.15; color: #14110a; background: var(--craie);
          border-radius: 16px 14px 16px 4px; box-shadow: 0 10px 30px -10px rgba(0,0,0,.7);
          opacity: 0; transform: translateY(6px) scale(.96); transform-origin: 0 50%; transition: opacity .35s, transform .35s;
        }
        .lp-bulle--dite { opacity: 1; transform: none; }
        @keyframes lp-appel { 0%,100% { box-shadow: 0 0 0 0 rgba(250,204,21,.55); } 50% { box-shadow: 0 0 0 12px rgba(250,204,21,0); } }
        .lp-ecoute { animation: lp-appel 1.8s ease-out infinite; }
        @media (min-width: 1024px) {
          .lp-tuteur { left: -26px; bottom: -226px; transform: none; }
          .lp-bulle { left: 178px; top: 96px; max-width: 360px; font-size: 1.15rem; }
        }
        /* Téléphone en paysage (~724 × 350) : le tableau tient dans la hauteur de l'écran, le tuteur et sa bulle
           se mettent à sa droite au lieu de dessous ; tout se voit d'un coup, sans défiler. */
        @media (max-height: 500px) and (orientation: landscape) and (max-width: 1023px) {
          .lp-plateau { max-width: calc((100svh - 140px) * 1.7778 + 20px); }
          .lp-tableau-zone { margin-bottom: 3rem; }
          /* au-dessus du bouton flottant du calendrier, en bas à droite de l'écran */
          .lp-tuteur { left: auto; right: 12px; bottom: 44px; transform: scale(.5); transform-origin: 100% 100%; }
          .lp-bulle { left: auto; right: 0; top: auto; bottom: 100%; max-width: 520px; font-size: 1.9rem; border-radius: 16px 14px 4px 16px; }
        }
        @media (prefers-reduced-motion: reduce) {
          .lp-monte, .lp-defile, .lp-trait::after { animation: none; }
          .lp-trait::after { clip-path: none; }
        }
      `}</style>

      {/* ═══ NAV ═══ */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-[#0a1410]/85 backdrop-blur-xl border-b border-white/10' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5">
            <LogoMoalim />
            <div>
              <div className="font-bold text-base leading-tight text-white">Moalim</div>
              <div className="text-[10px] text-white/50 leading-tight font-brand">معلم • ton prof au tableau</div>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-7 text-sm text-white/65">
            <a href="#animations" className="hover:text-yellow-300 transition">Animations</a>
            <a href="#tuteur" className="hover:text-yellow-300 transition">Le tuteur</a>
            <a href="#examens" className="hover:text-yellow-300 transition">Examens</a>
            <a href="#filieres" className="hover:text-yellow-300 transition">Filières</a>
            <a href="#faq" className="hover:text-yellow-300 transition">FAQ</a>
          </div>

          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <Link to="/dashboard" className="lp-btn px-4 py-2 text-sm">Mon tableau de bord</Link>
            ) : (
              <>
                <Link to="/login" className="hidden sm:inline-block px-3 py-2 text-sm text-white/70 hover:text-white transition">
                  Connexion
                </Link>
                <Link to="/inscription" className="lp-btn px-4 py-2 text-sm">
                  Commencer <ArrowRight className="w-4 h-4" />
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* D'abord le survol 3D des matières, puis le tableau vivant (26 novembre 2026) */}
      <Suspense fallback={<div className="h-screen" aria-hidden />}><VolDesMatieres /></Suspense>
      <HeroSection />
      <PromesseSection />
      <BandeMatieres />
      <CapacitesSection />
      <AnimationsSection />
      <ExamensSection />
      <FeaturesSection />
      <DashboardPreviewSection />
      <HowItWorksSection />
      <FilieresSection />
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

/** Le logo : la tête du tuteur dans son cadre d'ardoise bordé de craie jaune (la même image que l'icône d'onglet). */
function LogoMoalim({ taille = 40 }: { taille?: number }) {
  return (
    <span className="relative inline-block rounded-xl overflow-hidden shrink-0 bg-[#0f1d18] ring-2 ring-yellow-300 shadow-[0_3px_0_#a16207]"
      style={{ width: taille, height: taille }}>
      <img src="/media/avatar/moalim-tete.png" alt="Moalim" className="absolute left-1/2 top-[8%] w-[90%] max-w-none -translate-x-1/2" draggable={false} />
    </span>
  );
}

/** Le nombre de jours avant le bac, recalculé à minuit passé (la page peut rester ouverte). */
function useJours() {
  const [j, setJ] = useState(joursAvantBac());
  useEffect(() => {
    const t = setInterval(() => setJ(joursAvantBac()), 60_000);
    return () => clearInterval(t);
  }, []);
  return j;
}

/* ════════════════════════════════════════════════════════════
   HERO — le tableau vivant et le tuteur
   ════════════════════════════════════════════════════════════ */
function HeroSection() {
  const jours = useJours();
  return (
    <section id="accueil" className="relative pt-24 pb-10 sm:pt-28 z-10 scroll-mt-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 grid lg:grid-cols-[.86fr_1.14fr] gap-x-8 gap-y-7 items-start">
        {/* TEXTE — sur téléphone : texte, puis le tableau, puis les filières et les outils */}
        <div className="lp-monte lg:pt-6 lg:col-start-1 lg:row-start-1">
          <div className="inline-flex flex-wrap items-center gap-x-2 gap-y-1 px-3 py-1.5 rounded-full border border-white/15 bg-white/[.04] mb-6 text-xs">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
            </span>
            <span className="text-emerald-200">Année {ANNEE_SCOLAIRE}</span>
            <span className="text-white/30">·</span>
            <span className="text-white/80">Bac national : juin {BAC_YEAR}</span>
            {jours > 0 && <span className="px-1.5 py-0.5 rounded bg-rose-400 text-black font-black tabular-nums">J-{jours}</span>}
          </div>

          {/* Le mot de bienvenue, avant toute promesse */}
          <p className="craie text-2xl sm:text-3xl leading-none text-cyan-300 mb-3">
            <span className="font-brand font-bold text-[.8em]" dir="rtl">مرحبا بيك</span> 👋 Bienvenue. On commence de zéro, ensemble.
          </p>

          <h1 className="text-[2.5rem] sm:text-6xl lg:text-[3.5rem] xl:text-[4.1rem] font-black leading-[1.02] tracking-tight mb-5 text-white">
            Ton prof <span className="lp-trait">dessine</span> le cours
            <br />
            <span className="craie text-yellow-300 text-[1.12em] leading-none">devant toi.</span>
          </h1>

          <p className="text-lg text-white/70 leading-relaxed max-w-xl mb-7">
            Moalim explique <b className="text-white">en darija et en français</b>, anime chaque notion au tableau —
            <b style={{ color: MATIERE.maths }}> maths</b>,
            <b style={{ color: MATIERE.physique }}> physique-chimie</b>,
            <b style={{ color: MATIERE.svt }}> SVT</b> — puis t'entraîne sur les vrais sujets du national
            jusqu'au <b className="text-white">Bac {BAC_YEAR}</b>.
          </p>

          <div className="flex flex-col sm:flex-row gap-3">
            <Link to="/inscription" className="lp-btn px-7 py-4 text-base">
              Commencer gratuitement <ArrowRight className="w-5 h-5" />
            </Link>
            <a href="#animations" className="lp-btn-2 px-6 py-4 text-base">
              <Pencil className="w-4 h-4" /> Voir les animations
            </a>
          </div>

        </div>

        <div className="lp-monte order-3 lg:order-none lg:col-start-1 lg:row-start-2" style={{ animationDelay: '.25s' }}>
          {/* Filières : ce qui est là, ce qui arrive */}
          <a href="#filieres" className="flex flex-wrap items-center gap-2 text-xs mb-8 group">
            {['2ᵉ Bac PC', '2ᵉ Bac SVT'].map(f => (
              <span key={f} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-400/15 text-emerald-200 font-semibold">
                <Check className="w-3 h-3" /> {f}
              </span>
            ))}
            {['Sciences Maths', 'Sciences Éco'].map(f => (
              <span key={f} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full border border-dashed border-white/25 text-white/60">
                {f} <span className="craie text-yellow-300 text-sm leading-none">bientôt</span>
              </span>
            ))}
            <ArrowRight className="w-3.5 h-3.5 text-white/40 group-hover:translate-x-1 transition-transform" />
          </a>

          {/* Outils gratuits : deux portes d'entrée, sans voler la vedette au bouton principal */}
          <div className="grid sm:grid-cols-2 gap-2.5 max-w-xl">
            <Link to="/bac-diagnostic" className="lp-carte group flex items-center gap-3 px-3.5 py-3">
              <div className="w-9 h-9 rounded-xl bg-rose-400/20 flex items-center justify-center shrink-0">
                <Flame className="w-4 h-4 text-rose-300" />
              </div>
              <div className="min-w-0">
                <div className="text-sm font-semibold text-white leading-tight">Test diagnostic bac</div>
                <div className="text-[11px] text-white/55">Ta note estimée sur 20 · gratuit</div>
              </div>
              <ArrowRight className="w-4 h-4 text-white/30 ml-auto group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link to="/orientation" className="lp-carte group flex items-center gap-3 px-3.5 py-3">
              <div className="w-9 h-9 rounded-xl bg-cyan-400/20 flex items-center justify-center shrink-0">
                <Compass className="w-4 h-4 text-cyan-300" />
              </div>
              <div className="min-w-0">
                <div className="text-sm font-semibold text-white leading-tight">Orientation post-bac</div>
                <div className="text-[11px] text-white/55">Tes chances ENSA, ENCG, médecine…</div>
              </div>
              <ArrowRight className="w-4 h-4 text-white/30 ml-auto group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>

        {/* LE TABLEAU VIVANT */}
        <div className="lp-monte lp-tableau-zone relative mb-40 lg:mb-56 lg:pl-14 lg:col-start-2 lg:row-start-1 lg:row-span-2" style={{ animationDelay: '.15s' }}>
          <TableauVivant extraits={EXTRAITS} couleurs={COULEURS} />
          <p className="craie absolute right-1 -bottom-9 text-white/45 text-base rotate-[-2deg]">
            ↑ pas une vidéo : le vrai cours, la vraie voix
          </p>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   LA PROMESSE — le tuteur met en confiance, avec ses mots
   (26 novembre 2026 : « je veux commencer avec vous dès le zéro, c'est le temps de travailler,
   on va comprendre ensemble, je vais répondre à vos questions »)
   ════════════════════════════════════════════════════════════ */
/** Un mot clé de la promesse : il s'allume à son tour (`n`) quand la phrase arrive à l'écran. */
function Mot({ c, n, children }: { c: string; n: number; children: React.ReactNode }) {
  return <span className="lp-mot" style={{ ['--mot' as string]: c, ['--attente' as string]: `${.35 + n * .7}s` } as React.CSSProperties}>{children}</span>;
}

function PromesseSection() {
  // En darija seulement (26 novembre 2026) : le tuteur parle à l'élève dans sa langue.
  const [phrase, vue] = useVisible<HTMLParagraphElement>(0.3);
  const engagements = [
    { icon: Sprout, c: MATIERE.svt, titre: 'نبداو من الصفر', desc: 'عندك نقص؟ ماشي مشكل، غادي نعمروه. كل حاجة خاصك قبل الدرس، كنعاودو نشرحوها.' },
    { icon: Clock, c: MATIERE.maths, titre: 'هادا هو الوقت باش نخدمو', desc: 'شوية كل نهار، من دابا: فيونيو غادي توصل واجد، ماشي عيان.' },
    { icon: HeartHandshake, c: MATIERE.physique, titre: 'كنفهمو مع بعض', desc: 'ما كنحفظكش: كنرسم، كنخليك تجرب بيدك، وما كنزيدوش حتى يكون كلشي واضح.' },
    { icon: MessageCircle, c: '#f472b6', titre: 'كنجاوبك على أسئلتك', desc: 'كاملين. حتى السؤال اللي كتحشم تسولو فالقسم. شحال ما بغيتي من مرة.' },
  ];
  return (
    <section className="relative z-10 pb-16 sm:pb-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="lp-carte p-6 sm:p-10 [@media(max-height:500px)]:p-4" dir="rtl">
          <div className="flex flex-col md:flex-row [@media(max-height:500px)]:flex-row items-center md:items-start gap-5 md:gap-8 [@media(max-height:500px)]:gap-3 mb-8 [@media(max-height:500px)]:mb-3">
            <img src="/media/avatar/moalim-professeur.png" alt="" className="w-24 h-32 [@media(max-height:500px)]:w-14 [@media(max-height:500px)]:h-20 object-contain shrink-0 drop-shadow-xl" />
            <div className="text-center md:text-right [@media(max-height:500px)]:text-right">
              <div className="font-brand text-lg [@media(max-height:500px)]:text-[15px] leading-none text-cyan-300 mb-3 [@media(max-height:500px)]:mb-1">— الكلمة ديال معلم —</div>
              <p ref={phrase} className={`font-brand font-bold text-2xl sm:text-[2.2rem] [@media(max-height:500px)]:text-xl leading-[1.5] [@media(max-height:500px)]:leading-[1.45] text-white ${vue ? 'lp-mots-vus' : ''}`}>
                « غادي نبدا معاك <Mot c="#fde047" n={0}>من الصفر</Mot>. هادا هو الوقت باش نخدمو:
                غادي <Mot c="#6ee7b7" n={1}>نفهمو مع بعض</Mot>، وغادي نجاوبك على
                {' '}<Mot c="#fde047" n={2}>جميع الأسئلة ديالك</Mot>. »
              </p>
            </div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 [@media(max-height:500px)]:grid-cols-4 gap-4 [@media(max-height:500px)]:gap-2">
            {engagements.map(x => (
              <div key={x.titre} className="rounded-2xl bg-black/25 border border-white/10 p-4 [@media(max-height:500px)]:p-2.5">
                <div className="flex items-center gap-2.5 mb-2">
                  <div className="w-9 h-9 [@media(max-height:500px)]:hidden rounded-xl flex items-center justify-center shrink-0" style={{ background: `${x.c}22`, color: x.c }}>
                    <x.icon className="w-4.5 h-4.5" />
                  </div>
                  <h3 className="font-brand font-bold text-lg [@media(max-height:500px)]:text-[15px] text-white leading-tight">{x.titre}</h3>
                </div>
                <p className="font-brand text-[15px] text-white/70 leading-relaxed [@media(max-height:500px)]:leading-snug">{x.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   BANDE — les notions du programme défilent, écrites à la craie
   ════════════════════════════════════════════════════════════ */
function BandeMatieres() {
  const notions: [string, string][] = [
    ['lim f(x)', MATIERE.maths], ['ondes mécaniques', MATIERE.physique], ['sarcomère', MATIERE.svt], ['pH = pKa + log…', MATIERE.chimie],
    ['f ′(a)', MATIERE.maths], ['dipôle RC', MATIERE.physique], ['transcription', MATIERE.svt], ['vitesse de réaction', MATIERE.chimie],
    ['uₙ₊₁ = f(uₙ)', MATIERE.maths], ['diffraction', MATIERE.physique], ['glycolyse', MATIERE.svt], ['quotient Qr', MATIERE.chimie],
    ['ln x', MATIERE.maths], ['circuit RLC', MATIERE.physique], ['code génétique', MATIERE.svt], ['décroissance radioactive', MATIERE.physique],
  ];
  return (
    <section className="relative z-10 py-5 border-y border-white/10 bg-black/20 overflow-hidden" aria-hidden="true">
      <div className="lp-defile flex w-max gap-8 craie text-xl sm:text-2xl whitespace-nowrap">
        {[...notions, ...notions].map(([n, c], i) => (
          <span key={i} style={{ color: c }} className="opacity-80">{n} <span className="text-white/20 ml-8">✦</span></span>
        ))}
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   CAPACITÉS — ce que le tuteur sait faire
   ════════════════════════════════════════════════════════════ */
function CapacitesSection() {
  const items = [
    { icon: Pencil, c: MATIERE.maths, titre: 'Il dessine le cours devant toi',
      desc: "Pas de PDF, pas de vidéo figée : chaque notion se construit trait par trait au tableau, au moment où la voix l'explique.",
      motion: <svg viewBox="0 0 120 34" className="w-full h-9"><path d="M2 17 q 10 -18 20 0 t 20 0 t 20 0 t 20 0 t 20 0 t 20 0" fill="none" stroke={MATIERE.maths} strokeWidth="2.5" strokeLinecap="round" strokeDasharray="6 6" style={{ animation: 'lp-onde 1.4s linear infinite' }} /></svg> },
    { icon: Mic, c: MATIERE.svt, titre: 'Il parle ta langue',
      desc: 'Une vraie voix en darija, avec les termes du cours en français — comme ton meilleur prof, celui que tu comprends du premier coup.',
      motion: <div className="flex items-end gap-1 h-9">{[.5, .9, .6, 1, .7, .4, .85, .55, .95, .6, .8, .45].map((h, i) => <span key={i} className="w-1.5 rounded-full origin-bottom" style={{ height: `${h * 100}%`, background: MATIERE.svt, animation: `lp-barres ${0.7 + (i % 4) * 0.15}s ease-in-out ${i * 0.07}s infinite` }} />)}</div> },
    { icon: MessageCircle, c: MATIERE.physique, titre: 'Tu poses ta question, il répond au tableau',
      desc: "Écris, parle au micro ou envoie une photo de ton exercice : il s'arrête, t'explique sur le schéma, puis reprend le cours.",
      motion: <div className="flex items-center gap-2 h-9 craie text-lg"><span className="px-2.5 py-0.5 rounded-xl rounded-bl-sm bg-white/10 text-white/80">علاش τ = RC ؟</span><span style={{ color: MATIERE.physique, animation: 'lp-pulse 1.6s ease-in-out infinite' }}>✎ …</span></div> },
    { icon: FlaskConical, c: MATIERE.chimie, titre: 'Il te fait manipuler',
      desc: "Simulations que tu règles toi-même et labo virtuel en 3D : dosage, levures, sols… tu fais le TP, il commente ce que tu obtiens.",
      lien: { href: '/labo/', label: 'Ouvrir le labo 3D' },
      motion: <div className="flex items-end gap-2 h-9">{[60, 85, 40].map((h, i) => <span key={i} className="relative w-5 rounded-b-md border-2 border-t-0 border-white/40 h-full overflow-hidden"><span className="absolute inset-x-0 bottom-0 origin-bottom" style={{ height: `${h}%`, background: [MATIERE.chimie, '#f472b6', MATIERE.physique][i], opacity: .8, animation: `lp-barres ${2 + i * .4}s ease-in-out infinite` }} /></span>)}</div> },
    { icon: Trophy, c: '#f472b6', titre: 'Il corrige le national, question par question',
      desc: "Les vrais sujets, lus sur la feuille du jour J, puis démontrés pas à pas sur la figure du sujet — avec la méthode qui rapporte les points.",
      motion: <div className="flex items-center gap-1.5 h-9 craie text-lg">{['1-1', '1-2', '2-1', '2-2'].map((q, i) => <span key={q} className="px-2 py-0.5 rounded-lg border border-white/20" style={{ color: '#f472b6', animation: `lp-pulse 2.4s ease-in-out ${i * .6}s infinite` }}>{q}</span>)}</div> },
    { icon: NotebookPen, c: '#c084fc', titre: "Il retient ce que tu n'as pas compris",
      desc: 'Chaque réponse est notée par compétence. Tes lacunes reviennent plus tard, autrement, jusqu\'à ce qu\'elles tiennent — et ton cahier s\'écrit tout seul.',
      motion: <div className="flex items-center gap-1 h-9">{[1, 1, 1, 0, 1, 0, 1, 1, 1, 1].map((ok, i) => <span key={i} className="w-4 h-4 rounded-[5px]" style={ok ? { background: MATIERE.svt, opacity: .85 } : { background: '#f472b6', animation: 'lp-pulse 1.5s ease-in-out infinite' }} />)}</div> },
  ] as const;

  return (
    <section id="tuteur" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Ce que ton tuteur sait faire"
          title={<>Un prof particulier, <span className="craie text-yellow-300">pas un chatbot</span></>}
          subtitle="Il voit le tableau, il le montre du doigt, il lance les expériences et il s'arrête quand tu lèves la main."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-14">
          {items.map((it, i) => (
            <div key={i} className="lp-carte lp-leve p-6 flex flex-col">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0" style={{ background: `${it.c}22`, color: it.c }}>
                  <it.icon className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-white leading-snug">{it.titre}</h3>
              </div>
              <p className="text-sm text-white/65 leading-relaxed mb-5 flex-1">{it.desc}</p>
              <div className="pt-4 border-t border-dashed border-white/10 flex items-center justify-between gap-3">
                <div className="flex-1 min-w-0">{it.motion}</div>
                {'lien' in it && it.lien && (
                  <a href={it.lien.href} className="shrink-0 text-xs font-semibold inline-flex items-center gap-1 hover:underline" style={{ color: it.c }}>
                    {it.lien.label} <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   ANIMATIONS — une par matière, tirée du cours
   ════════════════════════════════════════════════════════════ */
function AnimationsSection() {
  const cartes = [
    { m: 'Maths', c: MATIERE.maths, icon: Sigma, cours: 'Suites numériques', titre: 'Les termes de uₙ₊₁ = f(uₙ) en escalier',
      src: `${SIM}/maths/suites-tableau/escalier.html`, mots: ['Limites', 'Dérivation', 'Suites', 'Primitives', 'ln', 'Complexes'] },
    { m: 'Physique', c: MATIERE.physique, icon: Atom, cours: 'Dipôle RC', titre: 'La craie trace la courbe de charge du condensateur',
      src: `${SIM}/physics/dipole-rc-tableau/courbe-charge.html`, mots: ['Ondes', 'Lumière', 'Radioactivité', 'RC', 'RL', 'RLC'] },
    { m: 'Chimie', c: MATIERE.chimie, icon: FlaskConical, cours: 'Acides et bases', titre: 'Le dosage, goutte après goutte',
      src: `${SIM}/chimie/acides-bases-tableau/dosage.html`, mots: ['Cinétique', 'Équilibre', 'Quotient Qr', 'pH · pKa', 'Dosage'] },
    { m: 'SVT', c: MATIERE.svt, icon: Leaf, cours: 'Relation gène – protéine', titre: "La traduction : de l'ARNm à la protéine",
      src: `${SIM}/svt/relation_gene_proteine-tableau/traduction.html`, mots: ['Respiration', 'Muscle', 'ADN', 'Transcription', 'Traduction'] },
  ];
  return (
    <section id="animations" className="relative z-10 py-20 sm:py-28 bg-black/20 border-y border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="La qualité, matière par matière"
          title={<>Des animations faites <span className="craie text-yellow-300">pour comprendre</span></>}
          subtitle="Ce que tu vois ici sort tel quel des cours : dessiné à la craie, peint quand c'est du vivant, toujours au rythme de l'explication."
        />
        <div className="grid md:grid-cols-2 gap-6 mt-14">
          {cartes.map(c => <CarteAnimation key={c.m} {...c} />)}
        </div>
        <p className="craie text-center text-white/50 text-lg mt-8">
          … et des centaines d'autres, une par notion du cadre de référence.
        </p>
      </div>
    </section>
  );
}

function CarteAnimation({ m, c, icon: Icon, cours, titre, src, mots }: {
  m: string; c: string; icon: any; cours: string; titre: string; src: string; mots: string[];
}) {
  const [ref, visible] = useVisible<HTMLDivElement>(0.35);
  const [tour, setTour] = useState(0);
  return (
    <div ref={ref} className="lp-carte overflow-hidden" style={{ borderColor: `${c}55` }}>
      <div className="flex items-center justify-between gap-3 px-4 py-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0" style={{ background: `${c}22`, color: c }}>
            <Icon className="w-4.5 h-4.5" />
          </div>
          <div className="min-w-0">
            <div className="craie text-xl leading-none" style={{ color: c }}>{m}</div>
            <div className="text-[11px] text-white/50 truncate">Cours « {cours} »</div>
          </div>
        </div>
        <button onClick={() => setTour(t => t + 1)} className="text-[11px] font-semibold px-2.5 py-1 rounded-full border border-white/20 text-white/70 hover:text-white hover:border-white/50 transition-colors shrink-0">
          ↻ Rejouer
        </button>
      </div>
      <div className="mx-2 rounded-lg overflow-hidden" style={{ background: 'radial-gradient(ellipse at 50% 35%,#13241e 0,#0f1d18 55%,#0a1410 100%)', boxShadow: 'inset 0 0 30px rgba(0,0,0,.5)' }}>
        <CadreAnimation src={src} titre={`${cours} — ${titre}`} actif={visible} cle={tour} />
      </div>
      <div className="px-4 py-3">
        <div className="text-sm font-semibold text-white mb-2">{titre}</div>
        <div className="flex flex-wrap gap-1.5">
          {mots.map(x => <span key={x} className="text-[11px] px-2 py-0.5 rounded-full bg-white/[.06] text-white/60">{x}</span>)}
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   EXAMENS RÉELS — « je connais tous les examens, on va tous les comprendre »
   Les en-têtes, les exercices et les figures viennent des sujets saisis (public/media/examens).
   ════════════════════════════════════════════════════════════ */
function ExamensSection() {
  const sujets = [
    { matiere: 'Physique-Chimie', code: 'NS 28F', coef: 7, c: MATIERE.physique, penche: 'lg:-rotate-2',
      figure: '/media/examens/physique/2025-normale/assets/fig3p5.png', legende: 'Figure 3 — la tension aux bornes du condensateur',
      exercices: [['Chimie', "Dosage d'une solution acide · suivi cinétique d'une estérification", '7 pts'],
        ['Transformations nucléaires', 'Désintégration du cadmium 107', '2,5 pts'],
        ['Électricité', "Charge et décharge d'un condensateur · démodulation", '5 pts'],
        ['Mécanique', "Mouvement d'un satellite · oscillateur mécanique", '5,5 pts']] },
    { matiere: 'Sciences de la Vie et de la Terre', code: 'NS 34F', coef: 5, c: MATIERE.svt, penche: 'lg:rotate-1',
      figure: '/media/examens/svt/2025-normale/assets/doc1p2.png', legende: 'Document 1 — le chou puant, sous la neige',
      exercices: [['Partie I', 'Restitution des connaissances', '5 pts'],
        ['Exercice 1', "Libération de l'énergie : le chou puant", '5 pts'],
        ['Exercice 2', "Expression et transmission de l'information génétique", '5 pts'],
        ['Exercice 3', 'Pollution des eaux souterraines', '5 pts']] },
    { matiere: 'Mathématiques', code: 'NS 22F', coef: 7, c: MATIERE.maths, penche: 'lg:-rotate-1',
      figure: null, legende: '',
      exercices: [['Exercice 1', "Géométrie dans l'espace", '3 pts'], ['Exercice 2', 'Nombres complexes', '3,5 pts'],
        ['Exercice 3', 'Calcul des probabilités', '2,5 pts'], ['Problème', "Étude d'une fonction — parties I, II et III", '11 pts']] },
  ];
  const annees = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];
  return (
    <section id="examens" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Les vrais sujets du national"
          title={<>Je connais <span className="craie text-yellow-300">tous les examens</span>.<br />On va tous les comprendre.</>}
          subtitle="60 sujets officiels, sessions normale et rattrapage, saisis question par question avec leurs figures. Voici ceux de juin 2025."
        />

        {/* Trois copies posées sur le tableau */}
        <div className="grid lg:grid-cols-3 gap-10 lg:gap-5 mt-14">
          {sujets.map(sj => (
            <article key={sj.matiere} className={`relative bg-[#fbfaf5] text-slate-900 rounded-sm shadow-[0_25px_60px_-15px_rgba(0,0,0,.85)] p-5 sm:p-6 transition-transform duration-300 hover:rotate-0 hover:-translate-y-2 ${sj.penche}`}
              style={{ fontFamily: "'Times New Roman', Times, serif" }}>
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 w-20 h-6 bg-yellow-200/80 rotate-[-2deg] shadow-sm" aria-hidden="true" />
              <header className="border-2 border-slate-900 text-center text-[12px] leading-tight mb-4">
                <div className="font-bold py-1 border-b border-slate-900">Examen National Unifié du Baccalauréat</div>
                <div className="grid grid-cols-[1fr_auto] divide-x divide-slate-900">
                  <div className="py-1 px-2">Session Normale 2025 · <b>{sj.matiere}</b></div>
                  <div className="py-1 px-2 font-bold">{sj.code}</div>
                </div>
                <div className="grid grid-cols-2 divide-x divide-slate-900 border-t border-slate-900">
                  <div className="py-1">Durée : 3 h</div>
                  <div className="py-1">Coefficient : {sj.coef}</div>
                </div>
              </header>
              <ol className="space-y-2 text-[14px] leading-snug">
                {sj.exercices.map(([t, d, pts]) => (
                  <li key={t + d} className="flex items-baseline gap-2">
                    <span className="flex-1"><b>{t}</b> — {d}</span>
                    <span className="shrink-0 text-[11px] font-bold border border-slate-900 px-1">{pts}</span>
                  </li>
                ))}
              </ol>
              {sj.figure
                ? <figure className="mt-4 pt-3 border-t border-dashed border-slate-400">
                    <img src={sj.figure} alt={sj.legende} loading="lazy" className="mx-auto max-h-36 object-contain mix-blend-multiply" />
                    <figcaption className="text-[12px] italic text-center mt-1 text-slate-600">{sj.legende}</figcaption>
                  </figure>
                : <div className="mt-4 pt-3 border-t border-dashed border-slate-400 text-center text-[14px] italic text-slate-700">
                    Limites, dérivée, tableau de variations, branches infinies, courbe, suite : le problème d'analyse, question par question.
                  </div>}
              {/* L'annotation du tuteur, à la craie de couleur sur la copie */}
              <div className="craie absolute -bottom-4 right-3 px-3 py-1 rounded-full text-base leading-none text-black shadow-lg rotate-[-3deg]" style={{ background: sj.c }}>
                corrigé pas à pas ✓
              </div>
            </article>
          ))}
        </div>

        {/* Toutes les années */}
        <div className="lp-carte mt-16 p-5 sm:p-7">
          <div className="flex flex-col lg:flex-row lg:items-center gap-4 lg:gap-6">
            <img src="/media/avatar/moalim-professeur.png" alt="" className="w-16 h-24 object-contain shrink-0 hidden lg:block" />
            <div className="flex-1 min-w-0">
              <p className="craie text-2xl sm:text-3xl leading-tight text-white mb-3">
                Dix ans de sujets, <span className="text-yellow-300">deux sessions par an</span>, trois matières.
              </p>
              <div className="flex flex-wrap gap-1.5">
                {annees.map(a => (
                  <span key={a} className="inline-flex items-center gap-1 pl-2.5 pr-1 py-1 rounded-full border border-white/15 bg-black/25 text-sm font-semibold text-white tabular-nums">
                    {a}
                    <span className="px-1.5 py-0.5 rounded-full bg-emerald-400/20 text-emerald-200 text-[10px] font-bold">N</span>
                    <span className="px-1.5 py-0.5 rounded-full bg-rose-400/20 text-rose-200 text-[10px] font-bold">R</span>
                  </span>
                ))}
              </div>
              <p className="text-sm text-white/60 mt-3">
                Pour chaque question : l'énoncé comme sur la feuille, la démonstration sur la figure du sujet, puis la rédaction qui rapporte les points.
              </p>
            </div>
            <Link to="/inscription" className="lp-btn px-5 py-3 text-sm shrink-0">S'entraîner sur un sujet <ArrowRight className="w-4 h-4" /></Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   MODES
   ════════════════════════════════════════════════════════════ */
function FeaturesSection() {
  return (
    <section id="features" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="4 façons d'apprendre"
          title={<>Choisis ton <span className="craie text-yellow-300">mode</span> selon ton objectif</>}
          subtitle="Du cours expliqué au tableau jusqu'aux concours des grandes écoles, Moalim s'adapte à ton niveau et à ton rythme."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-14">
          <FeatureCard c={MATIERE.maths} icon={Brain} tag="Mode Coaching"
            title="Teste ton niveau et progresse"
            desc="L'IA repère tes lacunes, construit un planning selon ton niveau et le temps qu'il reste avant le bac, et suit ta progression jour après jour."
            features={['Diagnostic de niveau initial', `Planning calé sur juin ${BAC_YEAR}`, 'Lacunes ciblées, reprises plus tard']} />
          <FeatureCard c={MATIERE.physique} icon={MessageCircle} tag="Mode Libre"
            title="Pose tes questions à n'importe quel moment"
            desc="Une formule à comprendre, une notion qui bloque ? Demande, il répond au tableau avec un exemple concret."
            features={['Français, arabe ou darija', 'Schémas dessinés à la demande', 'Disponible 24 h/24']} />
          <FeatureCard c="#f472b6" icon={Trophy} tag="Mode Examen réel"
            title="60 examens réels du bac, corrigés en direct"
            desc="Les sujets nationaux (sessions normale et rattrapage). Correction et explication immédiates, question par question."
            features={['60 sujets officiels', 'Correction + méthode', 'Bilan chapitre par chapitre']} />
          <FeatureCard c={MATIERE.svt} icon={School} tag="Mode Concours"
            title="Prépare les concours des grandes écoles"
            desc="Exercices et annales des concours marocains (ENSA, ENSAM, ENCG, médecine, CPGE…), chaque question expliquée."
            features={['Annales par concours', 'Explication interactive', 'Coaching stratégique']} />
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ c, icon: Icon, tag, title, desc, features }: {
  c: string; icon: any; tag: string; title: string; desc: string; features: string[];
}) {
  return (
    <div className="lp-carte lp-leve p-6">
      <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl mb-5" style={{ background: `${c}22`, color: c }}>
        <Icon className="w-7 h-7" />
      </div>
      <div className="craie text-lg leading-none mb-2" style={{ color: c }}>{tag}</div>
      <h3 className="text-xl font-bold mb-3 text-white">{title}</h3>
      <p className="text-sm text-white/60 leading-relaxed mb-5">{desc}</p>
      <ul className="space-y-2">
        {features.map((f, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-white/75">
            <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
            {f}
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ════════════════════════════════════════════════════════════
   TABLEAU DE BORD (maquette en JSX)
   ════════════════════════════════════════════════════════════ */
function DashboardPreviewSection() {
  return (
    <section id="dashboard" className="relative z-10 py-20 sm:py-28 bg-black/20 border-y border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Ton tableau de bord"
          title={<>Suis ta <span className="craie text-yellow-300">progression</span> en temps réel</>}
          subtitle="Chaque réponse, chaque exercice, chaque examen alimente ton bilan personnel."
        />
        <div className="mt-12 lp-carte overflow-hidden shadow-2xl shadow-black/60">
          <div className="flex items-center justify-between px-4 py-3 bg-black/40 border-b border-white/10">
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
    </section>
  );
}

function DashboardMock() {
  const sessions = [
    { mode: 'Coaching', subj: 'Dipôle RC — charge et décharge', time: 'Il y a 2 h', score: '92 %', c: MATIERE.physique },
    { mode: 'Examen', subj: 'PC — sujet national 2025 (normale)', time: 'Hier', score: '17/20', c: '#f472b6' },
    { mode: 'Libre', subj: 'Cinétique : facteurs et catalyse', time: 'Il y a 2 j', score: '—', c: MATIERE.chimie },
  ];
  return (
    <div className="bg-[#0a1410] p-4 sm:p-6 grid lg:grid-cols-[240px_1fr] gap-4">
      <aside className="hidden lg:flex flex-col gap-1 p-3 rounded-2xl bg-white/[.02] border border-white/5">
        <div className="flex items-center gap-2 p-3 mb-2">
          <LogoMoalim />
          <div>
            <div className="text-sm font-bold text-white">Moalim</div>
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
            it.active ? 'bg-yellow-300/15 text-yellow-200' : 'text-white/50'
          }`}>
            <it.icon className="w-4 h-4" />
            {it.label}
          </div>
        ))}
      </aside>

      <main className="space-y-4">
        <div className="rounded-2xl p-5 border border-white/10 bg-gradient-to-br from-emerald-500/15 via-transparent to-yellow-300/10 flex items-center justify-between flex-wrap gap-3">
          <div>
            <h3 className="text-lg sm:text-xl font-bold mb-1 text-white">Bon retour, Yasmine ✨</h3>
            <p className="text-sm text-white/60">Tu as <b className="text-white">3 notions à reprendre</b> en SVT avant de continuer</p>
          </div>
          <span className="px-4 py-2 rounded-xl bg-white/10 text-sm font-semibold flex items-center gap-2 text-white">
            Continuer ma séance <ArrowRight className="w-4 h-4" />
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: 'Heures', value: '47 h', delta: '+5 h', c: MATIERE.physique, icon: Clock },
            { label: 'Exercices', value: '128', delta: '+12', c: MATIERE.svt, icon: PenLine },
            { label: 'Score moyen', value: '15,8/20', delta: '+1,4', c: MATIERE.maths, icon: Trophy },
            { label: 'Série', value: '12 j', delta: '🔥', c: '#f472b6', icon: Zap },
          ].map((k, i) => (
            <div key={i} className="lp-carte p-4">
              <div className="w-9 h-9 rounded-xl flex items-center justify-center mb-2" style={{ background: `${k.c}22`, color: k.c }}>
                <k.icon className="w-4 h-4" />
              </div>
              <div className="text-[11px] text-white/50 font-medium">{k.label}</div>
              <div className="flex items-baseline gap-1.5">
                <span className="text-xl font-black text-white">{k.value}</span>
                <span className="text-[10px] text-emerald-400 font-bold">{k.delta}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-[1.3fr_1fr] gap-3">
          <div className="lp-carte p-4">
            <div className="flex items-center justify-between mb-3">
              <div>
                <div className="text-sm font-semibold text-white">Progression de la semaine</div>
                <div className="text-[11px] text-white/40">Heures par matière</div>
              </div>
              <div className="text-[10px] text-white/40">Cette semaine</div>
            </div>
            <div className="flex items-end gap-2 h-32">
              {[
                { d: 'L', svt: 60, pc: 40, math: 30 }, { d: 'M', svt: 45, pc: 70, math: 50 },
                { d: 'M', svt: 80, pc: 55, math: 60 }, { d: 'J', svt: 50, pc: 85, math: 40 },
                { d: 'V', svt: 65, pc: 60, math: 75 }, { d: 'S', svt: 90, pc: 70, math: 85 },
                { d: 'D', svt: 75, pc: 50, math: 60 },
              ].map((day, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-1 h-full">
                  <div className="w-full flex items-end gap-0.5 flex-1">
                    <div className="flex-1 rounded-t-sm" style={{ height: `${day.svt}%`, background: MATIERE.svt }} />
                    <div className="flex-1 rounded-t-sm" style={{ height: `${day.pc}%`, background: MATIERE.physique }} />
                    <div className="flex-1 rounded-t-sm" style={{ height: `${day.math}%`, background: MATIERE.maths }} />
                  </div>
                  <div className="text-[10px] text-white/40">{day.d}</div>
                </div>
              ))}
            </div>
            <div className="flex gap-3 mt-3 text-[10px] text-white/50">
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm" style={{ background: MATIERE.svt }} />SVT</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm" style={{ background: MATIERE.physique }} />PC</span>
              <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-sm" style={{ background: MATIERE.maths }} />Maths</span>
            </div>
          </div>

          <div className="lp-carte p-4 flex flex-col">
            <div className="text-sm font-semibold mb-1 text-white">Mention projetée</div>
            <div className="text-[11px] text-white/40 mb-3">D'après tes 6 dernières évaluations</div>
            <div className="flex-1 flex items-center justify-center relative">
              <svg className="w-32 h-32 -rotate-90">
                <circle cx="64" cy="64" r="52" stroke="rgba(255,255,255,.08)" strokeWidth="10" fill="none" />
                <circle cx="64" cy="64" r="52" stroke={MATIERE.maths} strokeWidth="10" fill="none"
                  strokeDasharray="326" strokeDashoffset="98" strokeLinecap="round" />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-3xl font-black text-yellow-300 leading-none">15,8</div>
                <div className="text-[10px] text-white/50 mt-1">/ 20</div>
              </div>
            </div>
            <div className="text-center mt-3">
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-300 text-[11px] font-bold">
                🏆 Mention Bien
              </span>
            </div>
          </div>
        </div>

        <div className="lp-carte p-4">
          <div className="text-sm font-semibold mb-3 text-white">Séances récentes</div>
          <div className="space-y-2">
            {sessions.map((s, i) => (
              <div key={i} className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/[.03]">
                <div className="w-9 h-9 rounded-xl flex items-center justify-center text-[10px] font-bold shrink-0" style={{ background: `${s.c}22`, color: s.c }}>
                  {s.mode.slice(0, 2).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold truncate text-white">{s.subj}</div>
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
   COMMENT ÇA MARCHE
   ════════════════════════════════════════════════════════════ */
function HowItWorksSection() {
  const steps = [
    { n: '1', icon: GraduationCap, title: 'Crée ton compte', desc: 'Inscription en 30 secondes, choisis ta filière et tes matières.' },
    { n: '2', icon: Target, title: 'Diagnostic', desc: "Le tuteur évalue ton niveau pour partir de là où tu en es vraiment." },
    { n: '3', icon: Pencil, title: 'Cours au tableau', desc: "Il t'explique, te fait manipuler, te pose des questions et corrige en direct." },
    { n: '4', icon: Trophy, title: 'Sujets du national', desc: 'Tu t\'entraînes sur les vrais sujets jusqu\'à viser ta mention.' },
  ];
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Comment ça marche"
          title={<>De zéro à la <span className="craie text-yellow-300">mention</span> en 4 étapes</>}
        />
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4 mt-12 relative">
          <div className="hidden md:block absolute top-12 left-[12.5%] right-[12.5%] border-t-2 border-dashed border-white/15" />
          {steps.map((s, i) => (
            <div key={i} className="relative lp-carte lp-leve p-5 text-center">
              <div className="w-14 h-14 rounded-full bg-[#0f1d18] border-2 border-yellow-300 text-yellow-300 mx-auto mb-4 flex items-center justify-center relative z-10">
                <s.icon className="w-6 h-6" />
              </div>
              <div className="craie text-lg text-yellow-300 leading-none mb-1">étape {s.n}</div>
              <h3 className="text-base font-bold mb-2 text-white">{s.title}</h3>
              <p className="text-xs text-white/60 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   FILIÈRES — ce qui est ouvert, ce qui arrive
   ════════════════════════════════════════════════════════════ */
function FilieresSection() {
  const filieres = [
    { nom: 'Sciences Physiques', sigle: '2ᵉ Bac PC · BIOF', etat: 'ouvert', c: MATIERE.physique, icon: Atom,
      detail: 'Physique, chimie, maths et SVT : cours animés, exercices, sujets du national.' },
    { nom: 'Sciences de la Vie et de la Terre', sigle: '2ᵉ Bac SVT · BIOF', etat: 'ouvert', c: MATIERE.svt, icon: Leaf,
      detail: 'SVT, physique-chimie et maths, avec les schémas à légender comme à l\'examen.' },
    { nom: 'Sciences Mathématiques', sigle: '2ᵉ Bac SM A et B', etat: 'bientot', c: MATIERE.maths, icon: Sigma,
      detail: 'Arithmétique, structures, analyse poussée : les mêmes animations, au niveau SM.' },
    { nom: 'Sciences Économiques', sigle: '2ᵉ Bac Éco et Gestion', etat: 'bientot', c: MATIERE.chimie, icon: TrendingUp,
      detail: 'Économie générale, comptabilité, maths : le tableau s\'ouvre aux filières éco.' },
  ];
  return (
    <section id="filieres" className="relative z-10 py-20 sm:py-28 bg-black/20 border-y border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Ta filière"
          title={<>PC et SVT aujourd'hui, <span className="craie text-yellow-300">les autres arrivent</span></>}
          subtitle="On ouvre une filière seulement quand chaque cours est animé, vérifié et aligné sur son cadre de référence."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-14">
          {filieres.map(f => {
            const ouvert = f.etat === 'ouvert';
            return (
              <div key={f.nom} className={`lp-carte lp-leve p-6 relative ${ouvert ? '' : 'border-dashed'}`} style={ouvert ? { borderColor: `${f.c}66` } : undefined}>
                <span className={`absolute -top-3 right-4 craie text-base leading-none px-2.5 py-1 rounded-full ${
                  ouvert ? 'bg-emerald-400 text-black' : 'bg-yellow-300 text-black rotate-3'}`}>
                  {ouvert ? '✓ ouvert' : 'bientôt'}
                </span>
                <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-4" style={{ background: `${f.c}22`, color: f.c, opacity: ouvert ? 1 : .75 }}>
                  <f.icon className="w-6 h-6" />
                </div>
                <div className="text-[11px] uppercase tracking-widest text-white/45 font-semibold mb-1">{f.sigle}</div>
                <h3 className="text-lg font-bold text-white leading-snug mb-2">{f.nom}</h3>
                <p className="text-sm text-white/60 leading-relaxed mb-4">{f.detail}</p>
                {ouvert ? (
                  <Link to="/inscription" className="inline-flex items-center gap-1 text-sm font-semibold hover:underline" style={{ color: f.c }}>
                    Commencer <ArrowRight className="w-4 h-4" />
                  </Link>
                ) : (
                  <Link to="/inscription" className="inline-flex items-center gap-1.5 text-sm font-semibold text-yellow-200 hover:underline">
                    <Bell className="w-4 h-4" /> Me prévenir à l'ouverture
                  </Link>
                )}
              </div>
            );
          })}
        </div>
        <p className="text-center text-sm text-white/50 mt-8">
          Tu es en Sciences Maths ou en Sciences Éco ? Inscris-toi dès maintenant : tu seras parmi les premiers prévenus.
        </p>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   CHIFFRES
   ════════════════════════════════════════════════════════════ */
function StatsSection() {
  const stats = [
    { v: '+1 200', l: 'élèves actif·ves', sub: 'partout au Maroc', c: MATIERE.maths },
    { v: '94 %', l: 'élèves satisfait·es', sub: 'note 4 ou 5/5', c: MATIERE.svt },
    { v: '+2,3', l: 'points en moyenne', sub: 'gagnés en 6 semaines', c: MATIERE.physique },
    { v: '24/7', l: 'disponibilité', sub: 'le tuteur ne dort pas', c: '#f472b6' },
  ];
  return (
    <section className="relative z-10 py-16 sm:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="lp-carte p-8 sm:p-12 grid sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 text-center">
          {stats.map((s, i) => (
            <div key={i}>
              <div className="craie text-6xl sm:text-7xl leading-none" style={{ color: s.c }}>{s.v}</div>
              <div className="text-sm font-semibold text-white mt-2">{s.l}</div>
              <div className="text-[11px] text-white/45 mt-1">{s.sub}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   TÉMOIGNAGES
   ════════════════════════════════════════════════════════════ */
function TestimonialsSection() {
  const items = [
    { name: 'Yasmine B.', school: 'Lycée Lalla Aïcha — Casablanca', subject: '2BAC PC BIOF', score: 'Physique 17.8/20', c: '#f472b6',
      quote: "J'avais peur des dipôles RLC mais le coaching IA explique au tableau étape par étape. En 2 mois j'ai gagné 3 points en physique." },
    { name: 'Mehdi A.', school: 'Lycée Mohammed VI — Rabat', subject: '2BAC PC BIOF', score: 'Chimie 18.2/20', c: MATIERE.physique,
      quote: "Les 60 examens réels avec correction instantanée, c'est dingue. Tu finis ta copie, tu reçois ta note + les commentaires question par question. Ça m'a sauvé pour le BAC." },
    { name: 'Salma K.', school: 'Lycée Al Khansaa — Fès', subject: '2BAC PC BIOF', score: 'Maths 16.5/20', c: MATIERE.maths,
      quote: "Je peux poser n'importe quelle question, même en darija, et l'IA répond avec des schémas. C'est comme avoir un prof particulier disponible 24h/24." },
    { name: 'Anas E.', school: 'Lycée Ibn Sina — Marrakech', subject: '2BAC PC BIOF', score: 'Moyenne 15.9/20', c: MATIERE.svt,
      quote: "L'orientation après chaque examen me dit exactement quel chapitre revoir. J'ai arrêté de réviser dans le vide, je cible mes points faibles." },
    { name: 'Nada R.', school: 'Lycée Al Farabi — Tanger', subject: '2BAC PC BIOF', score: 'Physique 17.1/20', c: '#c084fc',
      quote: "Les explications sur les ondes lumineuses sont claires, avec des schémas dessinés en direct sur le tableau. Même la diffraction devient évidente." },
    { name: 'Hamza T.', school: 'Lycée Hassan II — Agadir', subject: '2BAC PC BIOF', score: 'Maths 18.5/20', c: MATIERE.chimie,
      quote: "L'IA me fait travailler les démos étape par étape. Quand je bloque, elle reformule et donne des indices, jamais la réponse directe. Pédagogiquement c'est parfait." },
  ];
  return (
    <section id="testimonials" className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Témoignages"
          title={<>Ce que disent les <span className="craie text-yellow-300">bachelier·es</span></>}
          subtitle="Des élèves de toutes les villes du Maroc utilisent Moalim chaque jour."
        />
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-14">
          {items.map((t, i) => (
            <div key={i} className="lp-carte lp-leve p-6 relative">
              <Quote className="absolute top-4 right-4 w-6 h-6 text-white/10" />
              <div className="flex gap-0.5 mb-4">
                {[1, 2, 3, 4, 5].map(s => <Star key={s} className="w-4 h-4 fill-yellow-300 text-yellow-300" />)}
              </div>
              <p className="text-sm text-white/75 leading-relaxed mb-5">« {t.quote} »</p>
              <div className="flex items-center gap-3 pt-4 border-t border-dashed border-white/10">
                <div className="w-11 h-11 rounded-full flex items-center justify-center font-bold text-black shrink-0" style={{ background: t.c }}>
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
   PROGRAMME
   ════════════════════════════════════════════════════════════ */
function SubjectsSection() {
  const subjects = [
    { name: 'Physique', icon: Atom, c: MATIERE.physique, topics: [
      'Ondes mécaniques progressives et périodiques', 'Ondes lumineuses (diffraction, dispersion)', 'Décroissance radioactive',
      'Noyaux, masse et énergie', 'Dipôles RC, RL et circuit RLC', 'Lois de Newton · mouvements plans', 'Oscillateurs mécaniques'] },
    { name: 'Chimie', icon: FlaskConical, c: MATIERE.chimie, topics: [
      'Transformations lentes et rapides', 'Suivi temporel · vitesse de réaction', 'Transformations dans les deux sens',
      "État d'équilibre · quotient de réaction", 'Réactions acide-base · pH · pKa', 'Dosage acido-basique', 'Piles · électrolyse · estérification'] },
    { name: 'Mathématiques', icon: Calculator, c: MATIERE.maths, topics: [
      'Limites et continuité', 'Dérivation et étude des fonctions', 'Suites numériques', 'Fonctions primitives',
      'Fonctions logarithme et exponentielle', 'Nombres complexes', 'Calcul intégral · équations différentielles'] },
    { name: 'SVT', icon: Leaf, c: MATIERE.svt, topics: [
      "Réactions responsables de la libération d'énergie", 'Rôle du muscle strié squelettique', "Notion d'information génétique",
      'Relation gène – protéine', 'Génie génétique', 'Utilisation des matières organiques et inorganiques', 'Géodynamique interne'] },
  ];
  return (
    <section className="relative z-10 py-20 sm:py-28 bg-black/20 border-y border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <SectionHeader
          eyebrow="Cadre de référence officiel"
          title={<>Le programme de <span className="craie text-yellow-300">2ᵉ Bac</span>, rien de plus</>}
          subtitle="Chaque leçon suit le cadre de référence de l'examen national. Ce qui n'est pas à l'examen n'est pas dans le cours."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-12">
          {subjects.map((s, i) => (
            <div key={i} className="lp-carte p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ background: `${s.c}22`, color: s.c }}>
                  <s.icon className="w-6 h-6" />
                </div>
                <div className="craie text-2xl leading-none" style={{ color: s.c }}>{s.name}</div>
              </div>
              <ul className="space-y-1.5">
                {s.topics.map((t, j) => (
                  <li key={j} className="flex items-start gap-1.5 text-[13px] text-white/70 leading-snug">
                    <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   CONCOURS — bientôt
   ════════════════════════════════════════════════════════════ */
function ConcoursPrepSoonSection() {
  const concours = [
    { name: 'ENSA', desc: 'Écoles Nationales des Sciences Appliquées', icon: '⚙️' },
    { name: 'ENSAM', desc: "Arts et Métiers — ingénierie d'excellence", icon: '🔧' },
    { name: 'ENCG · TAFEM', desc: 'Écoles Nationales de Commerce et de Gestion', icon: '📊' },
    { name: 'Médecine · FMP', desc: 'Concours des facultés de médecine', icon: '⚕️' },
    { name: 'Architecture', desc: "Écoles Nationales d'Architecture", icon: '🏛️' },
    { name: 'CPGE', desc: 'Classes préparatoires aux grandes écoles', icon: '🎯' },
  ];
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid lg:grid-cols-[1fr_1.2fr] gap-10 lg:gap-14 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-yellow-300/40 bg-yellow-300/10 mb-5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-300 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-300" />
              </span>
              <span className="craie text-lg leading-none text-yellow-200">après le bac · bientôt</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-[1.08] tracking-tight mb-5 text-white">
              On ne s'arrête pas au bac.
              <br />
              <span className="craie text-yellow-300">La prépa concours arrive.</span>
            </h2>
            <p className="text-base text-white/65 leading-relaxed mb-6">
              Le tuteur connaît déjà ton profil, tes lacunes et tes forces : il prolonge la préparation
              vers les concours des grandes écoles marocaines, sans repartir de zéro.
            </p>
            <ul className="space-y-2.5 mb-7">
              {['Annales par concours, corrigées et commentées', 'QCM qui ciblent tes points faibles',
                'Simulations chronométrées au format du jour J', 'Un plan de préparation selon ton bac et ton concours'].map(b => (
                <li key={b} className="flex items-start gap-2 text-sm text-white/75">
                  <Check className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                  <span>{b}</span>
                </li>
              ))}
            </ul>
            <Link to="/orientation" className="lp-btn-2 px-5 py-3 text-sm">
              <Compass className="w-4 h-4" /> Calculer mes chances aux concours
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 sm:gap-4">
            {concours.map(c => (
              <div key={c.name} className="lp-carte lp-leve p-4 sm:p-5">
                <div className="text-2xl mb-2">{c.icon}</div>
                <h3 className="font-black text-white text-sm sm:text-base leading-tight mb-1">{c.name}</h3>
                <p className="text-xs text-white/55 leading-snug">{c.desc}</p>
              </div>
            ))}
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
    { q: "Est-ce vraiment gratuit pour commencer ?", a: "Oui. Tu peux créer un compte, suivre des séances et passer un examen réel sans aucune carte bancaire. Une fois que tu vois la valeur, tu peux passer au plan complet." },
    { q: "Quelles filières sont couvertes ?", a: "Aujourd'hui : la 2ᵉ année du baccalauréat Sciences Physiques (PC) et Sciences de la Vie et de la Terre (SVT), option française (BIOF). Les filières Sciences Mathématiques et Sciences Économiques sont en préparation : inscris-toi pour être prévenu·e à leur ouverture." },
    { q: "En quoi c'est différent d'une vidéo YouTube ou d'un chatbot ?", a: "Une vidéo ne s'arrête pas quand tu ne comprends plus, et un chatbot ne dessine pas. Ici le tuteur explique à voix haute en dessinant au tableau, te pose des questions, lance les simulations avec toi et répond à ta question sur le schéma — puis il reprend là où il s'était arrêté." },
    { q: "Combien d'examens du bac sont disponibles ?", a: "60 sujets réels du national — sessions normale et rattrapage. Chaque copie est corrigée et expliquée tout de suite, question par question, avec un bilan chapitre par chapitre." },
    { q: "Le tuteur parle-t-il en arabe ou en darija ?", a: "Oui. Les cours sont expliqués en darija, avec les termes scientifiques en français comme à l'examen. En mode libre tu peux écrire en français, en arabe ou en darija." },
    { q: "Puis-je l'utiliser sur mon téléphone ?", a: "Oui. Moalim fonctionne sur ordinateur, tablette et téléphone, sans rien installer. Sur téléphone, tourne l'écran en paysage pour voir le tableau en grand." },
    { q: "Mes données sont-elles en sécurité ?", a: "Les échanges sont chiffrés (HTTPS). Nous ne partageons jamais tes informations avec des tiers." },
  ];
  const [open, setOpen] = useState<number | null>(0);
  return (
    <section id="faq" className="relative z-10 py-20 sm:py-28 bg-black/20 border-y border-white/10">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        <SectionHeader eyebrow="FAQ" title={<>Tu as une <span className="craie text-yellow-300">question</span> ?</>} />
        <div className="space-y-3 mt-12">
          {faqs.map((f, i) => (
            <div key={i} className="lp-carte overflow-hidden">
              <button onClick={() => setOpen(open === i ? null : i)} aria-expanded={open === i}
                className="w-full flex items-center justify-between p-5 text-left">
                <span className="font-semibold text-sm sm:text-base pr-4 text-white">{f.q}</span>
                <ChevronDown className={`w-5 h-5 text-yellow-300 flex-shrink-0 transition-transform ${open === i ? 'rotate-180' : ''}`} />
              </button>
              <div className={`grid transition-all duration-300 ${open === i ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
                <div className="overflow-hidden">
                  <div className="px-5 pb-5 text-sm text-white/70 leading-relaxed">{f.a}</div>
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
   APPEL FINAL
   ════════════════════════════════════════════════════════════ */
function FinalCTASection() {
  const jours = useJours();
  return (
    <section className="relative z-10 py-20 sm:py-28">
      <div className="max-w-5xl mx-auto px-4 sm:px-6">
        <div className="relative rounded-2xl p-2.5 shadow-[0_30px_80px_-20px_rgba(0,0,0,.8)]"
          style={{ background: 'linear-gradient(160deg,#7a5836 0%,#5b4028 45%,#3f2c1b 100%)' }}>
          <div className="rounded-lg p-8 sm:p-14 text-center"
            style={{ background: 'radial-gradient(ellipse at 50% 35%,#16302a 0,#0f1d18 55%,#0a1410 100%)', boxShadow: 'inset 0 0 50px rgba(0,0,0,.55)' }}>
            {jours > 0 && <div className="craie text-2xl text-rose-300 mb-3">J-{jours} avant le bac {BAC_YEAR}</div>}
            <h2 className="craie text-5xl sm:text-7xl text-white leading-[.95] mb-5">
              Le tableau est prêt.<br /><span className="text-yellow-300">Il ne manque que toi.</span>
            </h2>
            <p className="text-base sm:text-lg text-white/75 max-w-xl mx-auto mb-8">
              Chaque semaine gagnée maintenant, c'est un chapitre de moins à rattraper en mai.
              Inscription gratuite, aucune carte requise.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link to="/inscription" className="lp-btn px-8 py-4">
                <GraduationCap className="w-5 h-5" /> Créer mon compte <ArrowRight className="w-5 h-5" />
              </Link>
              <Link to="/login" className="lp-btn-2 px-8 py-4">J'ai déjà un compte</Link>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 mt-8 text-xs text-white/60">
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-400" /> Sans carte bancaire</span>
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-400" /> Ordinateur et téléphone</span>
              <span className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-emerald-400" /> Darija et français</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ════════════════════════════════════════════════════════════
   PIED DE PAGE
   ════════════════════════════════════════════════════════════ */
function Footer() {
  return (
    <footer className="relative z-10 border-t border-white/10 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <LogoMoalim />
              <div className="font-bold text-white">Moalim</div>
            </div>
            <p className="text-xs text-white/50 leading-relaxed max-w-xs">
              Le tuteur IA des bachelier·es marocain·es : le cours dessiné au tableau, en darija et en français.
            </p>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Produit</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><a href="#animations" className="hover:text-white">Animations</a></li>
              <li><a href="#tuteur" className="hover:text-white">Le tuteur</a></li>
              <li><a href="#filieres" className="hover:text-white">Filières</a></li>
              <li><a href="/labo/" className="hover:text-white">Labo virtuel 3D</a></li>
              <li><Link to="/inscription" className="hover:text-white">Inscription</Link></li>
            </ul>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Ressources</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><Link to="/bac-diagnostic" className="hover:text-white">Test diagnostic bac</Link></li>
              <li><Link to="/orientation" className="hover:text-white">Orientation post-bac</Link></li>
              <li><a href="/blog/" className="hover:text-white">Blog</a></li>
              <li><a href="#faq" className="hover:text-white">FAQ</a></li>
              <li><a href="/about.html" className="hover:text-white">À propos</a></li>
            </ul>
          </div>
          <div>
            <div className="text-sm font-bold mb-3 text-white/80">Légal et contact</div>
            <ul className="space-y-2 text-xs text-white/50">
              <li><a href="/contact.html" className="hover:text-white">Contact</a></li>
              <li><a href="/mentions-legales.html" className="hover:text-white">Mentions légales</a></li>
              <li><a href="/mentions-legales.html#politique-confidentialite" className="hover:text-white">Confidentialité</a></li>
              <li><a href="/mentions-legales.html#cgu" className="hover:text-white">CGU</a></li>
            </ul>
          </div>
        </div>
        <div className="pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/40">
          <span>© {new Date().getFullYear()} Moalim · معلم — Fait avec ❤️ au Maroc 🇲🇦</span>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1"><Users className="w-3.5 h-3.5" /> Année {ANNEE_SCOLAIRE}</span>
            <span className="flex items-center gap-1"><Globe className="w-3.5 h-3.5" /> moalim.online</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

/* ════════════════════════════════════════════════════════════
   TITRE DE SECTION
   ════════════════════════════════════════════════════════════ */
function SectionHeader({ eyebrow, title, subtitle }: { eyebrow: string; title: React.ReactNode; subtitle?: string; }) {
  return (
    <div className="text-center max-w-2xl mx-auto">
      <div className="craie text-xl sm:text-2xl leading-none text-cyan-300 mb-3">— {eyebrow} —</div>
      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight mb-3 text-white">{title}</h2>
      {subtitle && <p className="text-base text-white/60 leading-relaxed">{subtitle}</p>}
    </div>
  );
}
