import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginStudent, getMe } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import { Eye, EyeOff, LogIn, AlertCircle } from 'lucide-react';

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
      // Persist tokens immediately so the axios interceptor attaches them to /auth/me
      localStorage.setItem('token', accessToken);
      if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
      // Fetch the real student record so the dashboard can greet them by name
      let student = {
        id: '',
        username: '',
        email,
        full_name: '',
        preferred_language: 'fr',
      };
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
      const errorMsg = err.response?.data?.detail || 'Erreur de connexion. Vérifiez vos identifiants.';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <img src="/media/logo.png" alt="معلم" className="h-16 w-auto mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-2 font-brand">معلم</h1>
          <p className="text-gray-600">Connecte-toi pour continuer ton apprentissage</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
          {/* Error Alert */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-red-800">Erreur de connexion</p>
                <p className="text-sm text-red-600 mt-1">{error}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                Adresse email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                placeholder="exemple@email.com"
                required
                autoComplete="email"
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                Mot de passe
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                  placeholder="••••••••"
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Connexion en cours...</span>
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5" />
                  <span>Se connecter</span>
                </>
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-gray-500">ou</span>
            </div>
          </div>

          {/* Sign Up Link */}
          <div className="text-center">
            <p className="text-gray-600">
              Pas encore de compte ?{' '}
              <Link 
                to="/signup" 
                className="font-semibold text-blue-600 hover:text-blue-700 transition-colors"
              >
                Créer un compte
              </Link>
            </p>
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
          <p className="text-sm font-medium text-blue-900 mb-2">Connexion</p>
          <p className="text-xs text-blue-700">
            Utilise un compte que tu as créé via l'inscription.
          </p>
          <p className="text-xs text-blue-700 mt-1">
            Si ton compte vient d'être créé, vérifie aussi la confirmation email si elle est activée dans Supabase.
          </p>
        </div>
      </div>
    </div>
  );
}
