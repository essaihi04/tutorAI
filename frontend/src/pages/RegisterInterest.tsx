import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap, Phone, MapPin, User, Mail, Sparkles,
  BookOpen, Brain, Mic, BarChart3, CheckCircle2, Clock,
  MessageCircle, ArrowRight, Star, ShieldCheck, Rocket
} from 'lucide-react';
import { submitRegistrationRequest } from '../services/api';

const WHATSAPP_NUMBER = '212641998700'; // international format without '+'
const WHATSAPP_DISPLAY = '+212 641 998 700';

function waLink(prefillText?: string) {
  const base = `https://wa.me/${WHATSAPP_NUMBER}`;
  return prefillText ? `${base}?text=${encodeURIComponent(prefillText)}` : base;
}

interface FormState {
  prenom: string;
  nom: string;
  phone: string;
  ville: string;
  email: string;
  promo_code: string;
  message: string;
}

const initialForm: FormState = {
  prenom: '',
  nom: '',
  phone: '',
  ville: '',
  email: '',
  promo_code: '',
  message: '',
};

export default function RegisterInterest() {
  const [form, setForm] = useState<FormState>(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  const onChange = (k: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
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
    if (err) {
      setError(err);
      return;
    }
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
      setError(
        err?.response?.data?.detail ||
          "Une erreur est survenue. Réessaie ou contacte-nous sur WhatsApp."
      );
    } finally {
      setLoading(false);
    }
  };

  // ─── SUCCESS / INFO VIEW ──────────────────────────────────────
  if (submitted) {
    return <SuccessView prenom={form.prenom} />;
  }

  // ─── FORM VIEW ────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-amber-50 relative overflow-hidden">
      {/* Decorative blobs */}
      <div className="absolute -top-40 -right-40 w-96 h-96 rounded-full bg-indigo-200/40 blur-3xl" />
      <div className="absolute -bottom-40 -left-40 w-96 h-96 rounded-full bg-amber-200/40 blur-3xl" />

      {/* Nav */}
      <nav className="relative flex items-center justify-between px-8 py-5 max-w-7xl mx-auto">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-200">
            <GraduationCap className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-extrabold bg-gradient-to-r from-indigo-700 to-purple-700 bg-clip-text text-transparent">
            معلم · Mou3allim
          </span>
        </Link>
        <Link
          to="/login"
          className="px-4 py-2 text-sm text-indigo-700 font-semibold hover:underline"
        >
          J'ai déjà un compte
        </Link>
      </nav>

      <div className="relative max-w-6xl mx-auto px-6 pb-20 pt-4 grid lg:grid-cols-2 gap-10 items-start">
        {/* LEFT — Hero */}
        <div className="space-y-6 lg:sticky lg:top-8">
          <div className="inline-flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-indigo-100">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span className="text-sm font-semibold text-indigo-700">
              BAC 2026 — inscription prioritaire
            </span>
          </div>

          <h1 className="text-4xl lg:text-5xl font-black text-gray-900 leading-tight">
            Démarre l'aventure.
            <br />
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-amber-500 bg-clip-text text-transparent">
              Le BAC en poche.
            </span>
          </h1>

          <p className="text-lg text-gray-600 leading-relaxed">
            Ton professeur IA personnel pour le 2<sup>ème</sup> BAC Sciences
            Physiques — disponible 24h/24, adapté à ton rythme, aux examens
            nationaux marocains.
          </p>

          <ul className="space-y-3">
            {[
              { icon: Brain, text: 'Cours + exercices adaptés à ton niveau' },
              { icon: BookOpen, text: 'Banque d\'examens nationaux corrigés (2016 → 2025)' },
              { icon: Mic, text: 'Dialogue vocal en français et darija' },
              { icon: BarChart3, text: 'Suivi de progression et révisions ciblées' },
            ].map((f, i) => (
              <li key={i} className="flex items-start gap-3">
                <div className="mt-0.5 w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                  <f.icon className="w-4 h-4 text-indigo-700" />
                </div>
                <span className="text-gray-700 pt-1">{f.text}</span>
              </li>
            ))}
          </ul>

          <div className="flex items-center gap-2 text-sm text-gray-500 pt-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            Tes informations restent confidentielles.
          </div>
        </div>

        {/* RIGHT — Form card */}
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-3xl shadow-xl shadow-indigo-100/50 border border-gray-100 p-6 sm:p-8 space-y-5"
        >
          <div className="text-center pb-2">
            <div className="inline-flex w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 items-center justify-center shadow-lg shadow-purple-200 mb-3">
              <Rocket className="w-7 h-7 text-white" />
            </div>
            <h2 className="text-2xl font-extrabold text-gray-900">
              Demande d'inscription
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              Remplis ce court formulaire. On te recontacte sous 24h.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <Field
              label="Prénom"
              icon={User}
              placeholder="Ahmed"
              value={form.prenom}
              onChange={onChange('prenom')}
              required
            />
            <Field
              label="Nom"
              icon={User}
              placeholder="El Amrani"
              value={form.nom}
              onChange={onChange('nom')}
              required
            />
          </div>

          <Field
            label="Téléphone (WhatsApp de préférence)"
            icon={Phone}
            placeholder="+212 6 00 00 00 00"
            value={form.phone}
            onChange={onChange('phone')}
            type="tel"
            required
          />

          <div className="grid sm:grid-cols-2 gap-4">
            <Field
              label="Ville"
              icon={MapPin}
              placeholder="Casablanca"
              value={form.ville}
              onChange={onChange('ville')}
              required
            />
            <Field
              label="Code promo (optionnel)"
              icon={Sparkles}
              placeholder="Ex: ECOLE123"
              value={form.promo_code}
              onChange={onChange('promo_code')}
            />
          </div>

          <Field
            label="Email (optionnel)"
            icon={Mail}
            placeholder="exemple@gmail.com"
            value={form.email}
            onChange={onChange('email')}
            type="email"
          />

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1.5">
              Un mot pour nous ? (optionnel)
            </label>
            <textarea
              value={form.message}
              onChange={onChange('message')}
              rows={3}
              placeholder="Ex: Je veux surtout renforcer la Physique…"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition outline-none resize-none"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl px-4 py-3">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-amber-500 text-white font-bold text-lg shadow-lg shadow-purple-200 hover:shadow-xl hover:scale-[1.01] active:scale-100 transition-all disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>Envoi en cours…</>
            ) : (
              <>
                <Rocket className="w-5 h-5" />
                Démarrer l'aventure · BAC en poche
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>

          <p className="text-center text-xs text-gray-400 pt-2">
            En envoyant ce formulaire, tu acceptes d'être contacté par
            l'équipe pour activer ton compte.
          </p>
        </form>
      </div>
    </div>
  );
}

// ─── Sub-components ──────────────────────────────────────────────

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
      <label className="block text-sm font-semibold text-gray-700 mb-1.5">
        {label}{required && <span className="text-red-500 ml-0.5">*</span>}
      </label>
      <div className="relative">
        <Icon className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition outline-none"
        />
      </div>
    </div>
  );
}

function SuccessView({ prenom }: { prenom: string }) {
  const waMsg = `Salam, je viens de m'inscrire sur Mou3allim (${prenom}). J'aimerais activer mon compte.`;
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-indigo-50">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header celebration */}
        <div className="bg-white rounded-3xl shadow-xl shadow-emerald-100/60 border border-gray-100 p-8 sm:p-10 text-center space-y-4">
          <div className="inline-flex w-20 h-20 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 items-center justify-center shadow-lg shadow-emerald-200 animate-[bounce_1s_ease-in-out_1]">
            <CheckCircle2 className="w-11 h-11 text-white" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-gray-900">
            Bienvenue, {prenom || 'futur bachelier'} ! 🎉
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ta demande a bien été reçue. Notre équipe te contactera très bientôt
            pour <strong className="text-indigo-700">activer ton compte</strong>.
          </p>

          {/* Contact row */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-3">
            <a
              href={waLink(waMsg)}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-[#25D366] hover:bg-[#1fbb57] text-white font-bold shadow-lg shadow-emerald-200 transition"
            >
              <MessageCircle className="w-5 h-5" />
              Nous contacter sur WhatsApp
            </a>
            <div className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-gray-100 text-gray-700 font-semibold">
              <Phone className="w-4 h-4" /> {WHATSAPP_DISPLAY}
            </div>
          </div>

          <div className="inline-flex items-center gap-2 text-sm text-gray-500 pt-3">
            <Clock className="w-4 h-4" />
            Délai habituel d'activation : moins de 24h.
          </div>
        </div>

        {/* What is this app */}
        <div className="mt-10 grid sm:grid-cols-2 gap-5">
          <InfoCard
            icon={Brain}
            title="Un tuteur IA qui t'écoute"
            color="indigo"
            desc="Pose tes questions à la voix ou au clavier, en français ou en darija. Il t'explique étape par étape, et reformule si tu n'as pas compris."
          />
          <InfoCard
            icon={BookOpen}
            title="Programme officiel + examens nationaux"
            color="amber"
            desc="Tous les chapitres du 2ème BAC SP BIOF, alignés sur le cadre de référence, avec les examens nationaux 2016 → 2025 corrigés."
          />
          <InfoCard
            icon={BarChart3}
            title="Plan d'étude personnalisé"
            color="purple"
            desc="Un diagnostic initial détecte tes forces et tes lacunes. L'app construit un planning adapté jusqu'au jour du BAC."
          />
          <InfoCard
            icon={Star}
            title="Exercices type BAC illimités"
            color="emerald"
            desc="Chaque leçon propose des exercices type BAC corrigés, avec la méthode et les pièges à éviter."
          />
        </div>

        {/* Steps */}
        <div className="mt-10 bg-white rounded-3xl shadow-lg border border-gray-100 p-7">
          <h2 className="text-xl font-bold text-gray-900 mb-5">La suite ?</h2>
          <ol className="space-y-4">
            {[
              { t: 'On te contacte', d: 'Par WhatsApp ou appel, sous 24h ouvrables.' },
              { t: 'On active ton compte', d: 'Tu reçois ton identifiant et ton mot de passe.' },
              { t: 'Tu te connectes & démarres', d: 'Diagnostic → plan d\'étude → première leçon. En avant !' },
            ].map((s, i) => (
              <li key={i} className="flex items-start gap-4">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 text-white font-bold flex items-center justify-center flex-shrink-0 shadow">
                  {i + 1}
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{s.t}</div>
                  <div className="text-sm text-gray-500">{s.d}</div>
                </div>
              </li>
            ))}
          </ol>
        </div>

        {/* Floating WhatsApp button fixed */}
        <a
          href={waLink(waMsg)}
          target="_blank"
          rel="noopener noreferrer"
          className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-[#25D366] hover:bg-[#1fbb57] shadow-2xl shadow-emerald-400/50 flex items-center justify-center transition hover:scale-110"
          aria-label="WhatsApp"
        >
          <MessageCircle className="w-7 h-7 text-white" />
        </a>

        <div className="text-center mt-8">
          <Link to="/" className="text-sm text-indigo-700 font-semibold hover:underline">
            ← Retour à l'accueil
          </Link>
        </div>
      </div>
    </div>
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
  const texts: Record<string, string> = {
    indigo: 'text-indigo-700',
    amber:  'text-amber-700',
    purple: 'text-purple-700',
    emerald:'text-emerald-700',
  };
  return (
    <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition">
      <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${grads[color]} flex items-center justify-center shadow mb-3`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      <h3 className={`font-bold ${texts[color]} mb-1.5`}>{title}</h3>
      <p className="text-sm text-gray-600 leading-relaxed">{desc}</p>
    </div>
  );
}
