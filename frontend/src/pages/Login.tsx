import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginStudent, getMe } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import { Eye, EyeOff, LogIn, AlertCircle, ArrowLeft } from 'lucide-react';
import MoalimShell, { MoalimLogo } from '../components/MoalimShell';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const login = useAuthStore((s) => s.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Veuillez remplir tous les champs');
      return;
    }
    setLoading(true);
    try {
      const res = await loginStudent({ email, password });
      const accessToken = res.data.access_token;
      const refreshToken = res.data.refresh_token;
      localStorage.setItem('token', accessToken);
      if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
      let student = { id: '', username: '', email, full_name: '', preferred_language: 'fr' };
      try {
        const meRes = await getMe();
        student = {
          id: String(meRes.data.id || ''),
          username: meRes.data.username || '',
          email: meRes.data.email || email,
          full_name: meRes.data.full_name || '',
          preferred_language: meRes.data.preferred_language || 'fr',
        };
      } catch (e) {
        console.warn('Failed to fetch student profile after login:', e);
      }
      login(accessToken, student, refreshToken);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur de connexion. Vérifiez vos identifiants.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <MoalimShell>
      {/* Top bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <Link to="/"><MoalimLogo /></Link>
        <Link to="/" className="text-sm text-white/50 hover:text-white flex items-center gap-1.5 transition">
          <ArrowLeft className="w-4 h-4" /> Retour
        </Link>
      </div>

      {/* Centered card */}
      <div className="flex items-center justify-center px-4 py-12 min-h-[calc(100vh-80px)]">
        <div className="w-full max-w-md anim-fade-up">
          <div className="text-center mb-8">
            <h1 className="text-3xl sm:text-4xl font-black mb-2">
              Bon retour <span className="gradient-text">parmi nous</span>
            </h1>
            <p className="text-white/55 text-sm">Connecte-toi pour reprendre ton apprentissage</p>
          </div>

          <div className="glass rounded-3xl p-7 shadow-2xl shadow-indigo-500/10">
            {error && (
              <div className="mb-5 p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start gap-2.5">
                <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm font-semibold text-rose-200">Erreur de connexion</p>
                  <p className="text-xs text-rose-300/80 mt-0.5">{error}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">
                  Adresse email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="moalim-input"
                  placeholder="exemple@email.com"
                  required
                  autoComplete="email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-xs font-semibold text-white/70 mb-2 uppercase tracking-wider">
                  Mot de passe
                </label>
                <div className="relative">
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="moalim-input pr-12"
                    placeholder="••••••••"
                    required
                    autoComplete="current-password"
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
              </div>

              <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Connexion en cours…</span>
                  </>
                ) : (
                  <>
                    <LogIn className="w-5 h-5" />
                    <span>Se connecter</span>
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
                Pas encore de compte ?{' '}
                <Link to="/inscription" className="font-semibold text-indigo-300 hover:text-indigo-200 transition">
                  Demander une inscription
                </Link>
              </p>
            </div>
          </div>

          <p className="text-center text-xs text-white/35 mt-6">
            Données chiffrées · Cadre de référence officiel 2BAC PC BIOF
          </p>
        </div>
      </div>
    </MoalimShell>
  );
}
