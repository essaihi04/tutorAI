import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Phone, MapPin, User, Mail, Sparkles, BookOpen, Brain, BarChart3,
  CheckCircle2, Clock, MessageCircle, ArrowRight, Star, ShieldCheck,
  Rocket, ArrowLeft, Trophy,
} from 'lucide-react';
import { submitRegistrationRequest } from '../services/api';
import MoalimShell, { MoalimLogo } from '../components/MoalimShell';

const WHATSAPP_NUMBER = '212641998700';
const WHATSAPP_DISPLAY = '+212 641 998 700';

function waLink(prefillText?: string) {
  const base = `https://wa.me/${WHATSAPP_NUMBER}`;
  return prefillText ? `${base}?text=${encodeURIComponent(prefillText)}` : base;
}

interface FormState {
  prenom: string; nom: string; phone: string; ville: string;
  email: string; promo_code: string; message: string;
}

const initialForm: FormState = {
  prenom: '', nom: '', phone: '', ville: '',
  email: '', promo_code: '', message: '',
};

export default function RegisterInterest() {
  const [form, setForm] = useState<FormState>(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const onChange = (k: keyof FormState) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
      setForm({ ...form, [k]: e.target.value });

  const validate = (): string | null => {
    if (form.prenom.trim().length < 2) return 'Prénom trop court';
    if (form.nom.trim().length < 2) return 'Nom trop court';
    if (form.phone.replace(/\D/g, '').length < 8) return 'Numéro de téléphone invalide';
    if (form.ville.trim().length < 2) return 'Ville requise';
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const err = validate();
    if (err) { setError(err); return; }
    setLoading(true);
    try {
      await submitRegistrationRequest({
        prenom: form.prenom.trim(),
        nom: form.nom.trim(),
        phone: form.phone.trim(),
        ville: form.ville.trim(),
        email: form.email.trim() || undefined,
        promo_code: form.promo_code.trim() ? form.promo_code.trim().toUpperCase() : undefined,
        message: form.message.trim() || undefined,
      });
      setSubmitted(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Une erreur est survenue. Réessaie ou contacte-nous sur WhatsApp.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) return <SuccessView prenom={form.prenom} />;

  return (
    <MoalimShell>
      {/* Top nav */}
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <Link to="/"><MoalimLogo /></Link>
        <div className="flex items-center gap-3">
          <Link to="/" className="hidden sm:flex items-center gap-1.5 text-sm text-white/50 hover:text-white transition">
            <ArrowLeft className="w-4 h-4" /> Retour
          </Link>
          <Link to="/login" className="px-4 py-2 text-sm text-white/70 hover:text-white transition">
            J'ai déjà un compte
          </Link>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 pb-20 pt-4 grid lg:grid-cols-[1fr_1.1fr] gap-10 items-start">
        {/* LEFT — Hero pitch */}
        <div className="space-y-6 lg:sticky lg:top-8 anim-fade-up">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-amber-200 font-semibold">BAC 2026 — inscription prioritaire</span>
          </div>

          <h1 className="text-4xl lg:text-5xl font-black leading-[1.05] tracking-tight">
            Démarre l'aventure.
            <br />
            <span className="gradient-text">Le BAC en poche.</span>
          </h1>

          <p className="text-base text-white/60 leading-relaxed">
            Ton tuteur IA personnel pour le 2<sup>ème</sup> BAC PC BIOF — adapté au cadre de
            référence officiel et aux 60 examens nationaux corrigés.
          </p>

          <ul className="space-y-3">
            {[
              { icon: Brain, text: 'Coaching IA adapté à ton niveau' },
              { icon: Trophy, text: '60 examens réels du BAC corrigés en direct' },
              { icon: BookOpen, text: 'Tous les chapitres officiels Physique · Chimie · Math' },
              { icon: BarChart3, text: 'Suivi de progression et révisions ciblées' },
            ].map((f, i) => (
              <li key={i} className="flex items-start gap-3">
                <div className="mt-0.5 w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-white/5 flex items-center justify-center flex-shrink-0">
                  <f.icon className="w-4 h-4 text-indigo-300" />
                </div>
                <span className="text-white/75 pt-1.5 text-sm">{f.text}</span>
              </li>
            ))}
          </ul>

          <div className="flex items-center gap-2 text-xs text-white/40 pt-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Tes informations restent confidentielles et chiffrées.
          </div>
        </div>

        {/* RIGHT — Form card */}
        <form
          onSubmit={handleSubmit}
          className="glass rounded-3xl p-6 sm:p-8 space-y-5 anim-fade-up shadow-2xl shadow-indigo-500/10"
          style={{ animationDelay: '.1s' }}
        >
          <div className="text-center pb-1">
            <div className="inline-flex w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-400 items-center justify-center shadow-lg shadow-indigo-500/40 mb-3">
              <Rocket className="w-7 h-7 text-white" />
            </div>
            <h2 className="text-2xl font-black text-white">Demande d'inscription</h2>
            <p className="text-sm text-white/50 mt-1">Remplis ce court formulaire — réponse sous 24h.</p>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <Field label="Prénom" icon={User} placeholder="Ahmed" value={form.prenom} onChange={onChange('prenom')} required />
            <Field label="Nom" icon={User} placeholder="El Amrani" value={form.nom} onChange={onChange('nom')} required />
          </div>

          <Field label="Téléphone (WhatsApp de préférence)" icon={Phone} placeholder="+212 6 00 00 00 00" value={form.phone} onChange={onChange('phone')} type="tel" required />

          <div className="grid sm:grid-cols-2 gap-4">
            <Field label="Ville" icon={MapPin} placeholder="Casablanca" value={form.ville} onChange={onChange('ville')} required />
            <Field label="Code promo (optionnel)" icon={Sparkles} placeholder="Ex : ECOLE123" value={form.promo_code} onChange={onChange('promo_code')} />
          </div>

          <Field label="Email (optionnel)" icon={Mail} placeholder="exemple@gmail.com" value={form.email} onChange={onChange('email')} type="email" />

          <div>
            <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">
              Un mot pour nous ? (optionnel)
            </label>
            <textarea
              value={form.message}
              onChange={onChange('message')}
              rows={3}
              placeholder="Ex : Je veux surtout renforcer la Physique…"
              className="moalim-input resize-none"
            />
          </div>

          {error && (
            <div className="rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-200 text-sm px-4 py-3">
              {error}
            </div>
          )}

          <button type="submit" disabled={loading} className="btn-primary w-full text-base py-4">
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Envoi en cours…
              </>
            ) : (
              <>
                <Rocket className="w-5 h-5" />
                Démarrer l'aventure
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>

          <p className="text-center text-[11px] text-white/35 pt-1">
            En envoyant ce formulaire, tu acceptes d'être contacté par l'équipe pour activer ton compte.
          </p>
        </form>
      </div>
    </MoalimShell>
  );
}

// ─── Field input avec icône ───────────────────────────────────
function Field({
  label, icon: Icon, value, onChange, placeholder, type = 'text', required,
}: {
  label: string;
  icon: any;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: string;
  required?: boolean;
}) {
  return (
    <div>
      <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">
        {label}{required && <span className="text-rose-400 ml-0.5">*</span>}
      </label>
      <div className="relative">
        <Icon className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40 pointer-events-none" />
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className="moalim-input pl-10"
        />
      </div>
    </div>
  );
}

// ─── Vue de succès ────────────────────────────────────────────
function SuccessView({ prenom }: { prenom: string }) {
  const waMsg = `Salam, je viens de m'inscrire sur Moalim (${prenom}). J'aimerais activer mon compte.`;
  return (
    <MoalimShell>
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
        <Link to="/"><MoalimLogo /></Link>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 anim-fade-up">
        {/* Hero celebration */}
        <div className="glass rounded-3xl p-8 sm:p-10 text-center space-y-4 shadow-2xl shadow-emerald-500/10">
          <div className="inline-flex w-20 h-20 rounded-3xl bg-gradient-to-br from-emerald-500 to-teal-500 items-center justify-center shadow-2xl shadow-emerald-500/40 anim-float">
            <CheckCircle2 className="w-11 h-11 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white">
            Bienvenue, {prenom || 'futur bachelier'} ! 🎉
          </h1>
          <p className="text-base sm:text-lg text-white/65 max-w-2xl mx-auto">
            Ta demande a bien été reçue. Notre équipe te contactera très bientôt pour{' '}
            <strong className="text-emerald-300">activer ton compte</strong>.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-3">
            <a
              href={waLink(waMsg)}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-[#25D366] hover:bg-[#1fbb57] text-white font-bold shadow-2xl shadow-emerald-500/30 transition"
            >
              <MessageCircle className="w-5 h-5" />
              Nous contacter sur WhatsApp
            </a>
            <div className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl glass text-white font-semibold">
              <Phone className="w-4 h-4 text-emerald-400" /> {WHATSAPP_DISPLAY}
            </div>
          </div>

          <div className="inline-flex items-center gap-2 text-sm text-white/45 pt-3">
            <Clock className="w-4 h-4" />
            Délai habituel d'activation : moins de 24h.
          </div>
        </div>

        {/* What you get */}
        <div className="mt-8 grid sm:grid-cols-2 gap-4">
          <InfoCard icon={Brain} color="indigo" title="Tuteur IA pédagogique" desc="Pose tes questions au clavier en français, arabe ou darija. L'IA t'explique étape par étape, et reformule si besoin." />
          <InfoCard icon={Trophy} color="amber" title="60 examens réels du BAC" desc="Tous les sujets nationaux récents (sessions normale + rattrapage), corrigés et expliqués instantanément avec feedback et orientation." />
          <InfoCard icon={BookOpen} color="purple" title="Cadre de référence officiel" desc="Tous les chapitres du 2BAC PC BIOF — Physique, Chimie, Mathématiques — alignés avec le référentiel du Ministère." />
          <InfoCard icon={BarChart3} color="emerald" title="Plan d'étude personnalisé" desc="Un diagnostic initial détecte tes forces et lacunes. L'app construit un planning adapté jusqu'au jour du BAC." />
        </div>

        {/* Steps */}
        <div className="mt-8 glass rounded-3xl p-6 sm:p-7">
          <h2 className="text-lg font-bold text-white mb-5">La suite ?</h2>
          <ol className="space-y-4">
            {[
              { t: 'On te contacte', d: 'Par WhatsApp ou appel, sous 24h ouvrables.' },
              { t: 'On active ton compte', d: 'Tu reçois ton identifiant et ton mot de passe.' },
              { t: 'Tu te connectes & démarres', d: 'Diagnostic → plan d\'étude → première leçon. En avant !' },
            ].map((s, i) => (
              <li key={i} className="flex items-start gap-4">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 text-white font-bold flex items-center justify-center flex-shrink-0 shadow-lg shadow-indigo-500/30">
                  {i + 1}
                </div>
                <div>
                  <div className="font-semibold text-white">{s.t}</div>
                  <div className="text-sm text-white/55">{s.d}</div>
                </div>
              </li>
            ))}
          </ol>
        </div>

        {/* Floating WhatsApp */}
        <a
          href={waLink(waMsg)}
          target="_blank"
          rel="noopener noreferrer"
          className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-[#25D366] hover:bg-[#1fbb57] shadow-2xl shadow-emerald-500/50 flex items-center justify-center transition hover:scale-110 z-50"
          aria-label="WhatsApp"
        >
          <MessageCircle className="w-7 h-7 text-white" />
        </a>

        <div className="text-center mt-8">
          <Link to="/" className="text-sm text-indigo-300 hover:text-indigo-200 transition">
            ← Retour à l'accueil
          </Link>
        </div>
      </div>
    </MoalimShell>
  );
}

function InfoCard({ icon: Icon, title, desc, color }: {
  icon: any; title: string; desc: string;
  color: 'indigo' | 'amber' | 'purple' | 'emerald';
}) {
  const grads: Record<string, string> = {
    indigo: 'from-indigo-500 to-blue-600',
    amber:  'from-amber-500 to-orange-500',
    purple: 'from-purple-500 to-fuchsia-600',
    emerald:'from-emerald-500 to-teal-600',
  };
  return (
    <div className="tilt-card glass rounded-2xl p-5">
      <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${grads[color]} flex items-center justify-center shadow-lg mb-3`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      <h3 className="font-bold text-white mb-1.5 text-sm">{title}</h3>
      <p className="text-xs text-white/60 leading-relaxed">{desc}</p>
    </div>
  );
}

// Keep used import warning silenced
void Star;
