import { useState, useMemo } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerStudent } from '../services/api';
import { Eye, EyeOff, UserPlus, AlertCircle, CheckCircle2, Globe, ArrowLeft } from 'lucide-react';
import MoalimShell, { MoalimLogo } from '../components/MoalimShell';

interface FormData {
  username: string;
  email: string;
  password: string;
  full_name: string;
  preferred_language: string;
}

export default function Signup() {
  const [form, setForm] = useState<FormData>({
    username: '', email: '', password: '', full_name: '', preferred_language: 'fr',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const passwordStrength = useMemo(() => {
    const password = form.password;
    if (!password) return { strength: 0, label: '', color: 'bg-white/10' };
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    if (strength <= 1) return { strength, label: 'Faible', color: 'bg-rose-500' };
    if (strength <= 3) return { strength, label: 'Moyen', color: 'bg-amber-400' };
    return { strength, label: 'Fort', color: 'bg-emerald-400' };
  }, [form.password]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!form.full_name || !form.username || !form.email || !form.password) {
      setError('Veuillez remplir tous les champs');
      return;
    }
    if (form.password.length < 6) {
      setError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }
    if (form.username.length < 3) {
      setError("Le nom d'utilisateur doit contenir au moins 3 caractères");
      return;
    }
    setLoading(true);
    try {
      await registerStudent(form);
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erreur lors de l'inscription. Veuillez réessayer.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <MoalimShell>
        <div className="flex items-center justify-center min-h-screen px-4">
          <div className="w-full max-w-md glass rounded-3xl p-10 text-center anim-fade-up">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-emerald-500/15 mb-4">
              <CheckCircle2 className="w-9 h-9 text-emerald-400" />
            </div>
            <h2 className="text-2xl font-black text-white mb-2">Compte créé !</h2>
            <p className="text-white/60 mb-3">Bienvenue sur Moalim. Tu vas pouvoir te connecter.</p>
            <p className="text-xs text-white/40">Redirection automatique…</p>
          </div>
        </div>
      </MoalimShell>
    );
  }

  return (
    <MoalimShell>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <Link to="/"><MoalimLogo /></Link>
        <Link to="/" className="text-sm text-white/50 hover:text-white flex items-center gap-1.5 transition">
          <ArrowLeft className="w-4 h-4" /> Retour
        </Link>
      </div>

      <div className="flex items-center justify-center px-4 py-10 min-h-[calc(100vh-80px)]">
        <div className="w-full max-w-md anim-fade-up">
          <div className="text-center mb-7">
            <h1 className="text-3xl sm:text-4xl font-black mb-2">
              Crée ton <span className="gradient-text">compte Moalim</span>
            </h1>
            <p className="text-white/55 text-sm">
              Rejoins les bachelier·es 2BAC PC BIOF qui révisent intelligemment
            </p>
          </div>

          <div className="glass rounded-3xl p-7 shadow-2xl shadow-indigo-500/10">
            {error && (
              <div className="mb-5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-2.5">
                <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-rose-300/90">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <FormField label="Nom complet" name="full_name" value={form.full_name} onChange={handleChange} placeholder="Ahmed Benali" required />
              <FormField label="Nom d'utilisateur" name="username" value={form.username} onChange={handleChange} placeholder="ahmed_benali" required minLength={3} />
              <FormField label="Adresse email" name="email" type="email" value={form.email} onChange={handleChange} placeholder="ahmed@example.com" required />

              <div>
                <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">Mot de passe</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    className="moalim-input pr-12"
                    placeholder="••••••••"
                    required
                    minLength={6}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-white/50 hover:text-white transition"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {form.password && (
                  <div className="mt-2">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                        <div className={`h-full transition-all ${passwordStrength.color}`} style={{ width: `${(passwordStrength.strength / 5) * 100}%` }} />
                      </div>
                      <span className="text-[11px] font-medium text-white/60">{passwordStrength.label}</span>
                    </div>
                  </div>
                )}
              </div>

              <div>
                <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">
                  <Globe className="w-3.5 h-3.5 inline mr-1" /> Langue préférée
                </label>
                <select
                  name="preferred_language"
                  value={form.preferred_language}
                  onChange={handleChange}
                  className="moalim-input"
                >
                  <option value="fr" className="bg-[#0b0b1d]">🇫🇷 Français</option>
                  <option value="ar" className="bg-[#0b0b1d]">🇲🇦 العربية (Arabe)</option>
                  <option value="mixed" className="bg-[#0b0b1d]">🌍 Bilingue (Français/Arabe)</option>
                </select>
              </div>

              <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Création du compte…</span>
                  </>
                ) : (
                  <>
                    <UserPlus className="w-5 h-5" />
                    <span>Créer mon compte</span>
                  </>
                )}
              </button>
            </form>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10" />
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="px-4 bg-[#070718] text-white/40 uppercase tracking-widest">ou</span>
              </div>
            </div>

            <div className="text-center">
              <p className="text-sm text-white/55">
                Déjà un compte ?{' '}
                <Link to="/login" className="font-semibold text-indigo-300 hover:text-indigo-200 transition">
                  Se connecter
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </MoalimShell>
  );
}

function FormField({
  label, name, value, onChange, placeholder, type = 'text', required, minLength,
}: {
  label: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: string;
  required?: boolean;
  minLength?: number;
}) {
  return (
    <div>
      <label className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">{label}</label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        className="moalim-input"
        placeholder={placeholder}
        required={required}
        minLength={minLength}
      />
    </div>
  );
}
