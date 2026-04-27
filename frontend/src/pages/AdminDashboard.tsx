import { useState, useEffect, useCallback } from 'react';
import {
  Shield, Users, DollarSign, Activity, Wifi, WifiOff,
  Plus, Trash2, Key, Search, RefreshCw, LogOut,
  ChevronDown, ChevronUp, Eye, EyeOff, X, Check,
  Clock, Zap, BarChart3, TrendingUp, Server, AlertCircle,
  UserPlus, Lock, Mail, User, FileUp,
  MessageCircle, MapPin, Phone, Inbox
} from 'lucide-react';
import {
  adminLogin, getAdminDashboard, getAdminUsers, createAdminUser,
  updateAdminUser, deleteAdminUser, bulkUserAction, resetUserPassword, getOnlineUsers,
  getUsageSummary, getUsageByUser, getRecentRequests,
  listRegistrationRequests, updateRegistrationRequest, deleteRegistrationRequest,
  activateRegistration, listPromoCodes, createPromoCode, updatePromoCode, deletePromoCode
} from '../services/api';

// ─── Types ───────────────────────────────────────────────────
interface DashboardStats {
  total_users: number;
  active_users: number;
  online_count: number;
  online_user_ids: string[];
  today: { cost_usd: number; requests: number; tokens: number };
  this_month: { cost_usd: number; tokens: number };
  all_time_cost_usd: number;
}

interface UserRecord {
  id: string;
  username: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_admin: boolean;
  is_online: boolean;
  created_at: string;
  expires_at?: string | null;
  preferred_language: string;
  promo_code?: string | null;
}

interface ProviderStats {
  requests: number;
  tokens: number;
  cost_usd: number;
}

interface UsageSummary {
  period_days: number;
  total_cost_usd: number;
  total_requests: number;
  total_tokens: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  providers: Record<string, ProviderStats>;
  daily: Record<string, { requests: number; tokens: number; cost_usd: number }>;
}

interface UserUsage {
  student_id: string;
  student_email: string;
  full_name: string;
  username: string;
  requests: number;
  total_tokens: number;
  prompt_tokens: number;
  completion_tokens: number;
  cost_usd: number;
  providers: Record<string, ProviderStats>;
  last_request: string;
}

interface RecentRequest {
  id: string;
  student_email: string;
  provider: string;
  model: string;
  endpoint: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  cost_usd: number;
  request_duration_ms: number;
  session_type: string;
  created_at: string;
}

// ─── Helper Components ───────────────────────────────────────

function StatCard({ icon: Icon, label, value, sub, color }: {
  icon: any; label: string; value: string | number; sub?: string; color: string;
}) {
  return (
    <div className="bg-white rounded-xl sm:rounded-2xl p-3 sm:p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="text-[11px] sm:text-sm text-gray-500 font-medium truncate">{label}</p>
          <p className="text-lg sm:text-2xl font-bold text-gray-900 mt-0.5 sm:mt-1 truncate">{value}</p>
          {sub && <p className="text-[10px] sm:text-xs text-gray-400 mt-0.5 sm:mt-1 truncate">{sub}</p>}
        </div>
        <div className={`p-2 sm:p-3 rounded-lg sm:rounded-xl flex-shrink-0 ${color}`}>
          <Icon className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
        </div>
      </div>
    </div>
  );
}

function ProviderBadge({ provider }: { provider: string }) {
  const colors: Record<string, string> = {
    deepseek: 'bg-blue-100 text-blue-700',
    mistral_ocr: 'bg-purple-100 text-purple-700',
    mistral_chat: 'bg-indigo-100 text-indigo-700',
    gemini: 'bg-green-100 text-green-700',
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${colors[provider] || 'bg-gray-100 text-gray-700'}`}>
      {provider}
    </span>
  );
}

// ─── Login Screen ────────────────────────────────────────────

function AdminLoginScreen({ onLogin }: { onLogin: () => void }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPw, setShowPw] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await adminLogin(password);
      localStorage.setItem('admin_token', res.data.access_token);
      onLogin();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Mot de passe incorrect');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-red-600 rounded-2xl mb-4">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
          <p className="text-gray-400 mt-2">معلم — Panneau d'administration</p>
        </div>
        <div className="bg-gray-800 rounded-2xl p-8 border border-gray-700 shadow-2xl">
          {error && (
            <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded-xl flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <p className="text-sm text-red-300">{error}</p>
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Mot de passe admin</label>
              <div className="relative">
                <input
                  type={showPw ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-xl text-white focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none"
                  placeholder="••••••••"
                  autoFocus
                />
                <button type="button" onClick={() => setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-200">
                  {showPw ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-3 bg-red-600 text-white rounded-xl font-semibold hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Lock className="w-5 h-5" />}
              {loading ? 'Connexion...' : 'Accéder au dashboard'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

// ─── Create User Modal ───────────────────────────────────────

function CreateUserModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [form, setForm] = useState({ email: '', password: '', full_name: '', username: '', promo_code: '', is_admin: false });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPw, setShowPw] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (!form.email || !form.password || !form.full_name || !form.username) {
      setError('Tous les champs sont obligatoires');
      return;
    }
    setLoading(true);
    try {
      await createAdminUser(form);
      onCreated();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur lors de la création');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold flex items-center gap-2">
            <UserPlus className="w-5 h-5 text-blue-600" /> Créer un compte
          </h3>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded-lg"><X className="w-5 h-5" /></button>
        </div>
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{error}</div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nom complet</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input type="text" value={form.full_name} onChange={e => setForm({ ...form, full_name: e.target.value })}
                  className="w-full pl-10 pr-3 py-2.5 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ahmed Benali" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input type="text" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })}
                className="w-full px-3 py-2.5 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="ahmed_b" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
                className="w-full pl-10 pr-3 py-2.5 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="email@example.com" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input type={showPw ? 'text' : 'password'} value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })}
                className="w-full pl-10 pr-10 py-2.5 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Min. 6 caractères" />
              <button type="button" onClick={() => setShowPw(!showPw)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Code promo</label>
            <div className="relative">
              <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input type="text" value={form.promo_code} onChange={e => setForm({ ...form, promo_code: e.target.value })}
                className="w-full pl-10 pr-3 py-2.5 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none uppercase" placeholder="Ex: ECOLE123" />
            </div>
          </div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={form.is_admin} onChange={e => setForm({ ...form, is_admin: e.target.checked })}
              className="w-4 h-4 rounded text-red-600 focus:ring-red-500" />
            <span className="text-sm text-gray-700">Compte administrateur</span>
          </label>
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose}
              className="flex-1 py-2.5 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50">Annuler</button>
            <button type="submit" disabled={loading}
              className="flex-1 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2">
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
              Créer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ─── Reset Password Modal ────────────────────────────────────

function ResetPasswordModal({ userId, userName, onClose }: { userId: string; userName: string; onClose: () => void }) {
  const [newPw, setNewPw] = useState('');
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState('');

  const handleReset = async () => {
    if (newPw.length < 6) { setError('Minimum 6 caractères'); return; }
    setLoading(true);
    try {
      await resetUserPassword(userId, newPw);
      setDone(true);
      setTimeout(onClose, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 w-full max-w-sm shadow-2xl" onClick={e => e.stopPropagation()}>
        <h3 className="text-lg font-bold mb-4">Réinitialiser le mot de passe</h3>
        <p className="text-sm text-gray-500 mb-4">Pour: <strong>{userName}</strong></p>
        {done ? (
          <div className="p-4 bg-green-50 rounded-xl text-green-700 flex items-center gap-2">
            <Check className="w-5 h-5" /> Mot de passe réinitialisé!
          </div>
        ) : (
          <>
            {error && <div className="mb-3 p-2 bg-red-50 rounded-lg text-sm text-red-600">{error}</div>}
            <input type="text" value={newPw} onChange={e => setNewPw(e.target.value)}
              className="w-full px-3 py-2.5 border rounded-xl mb-4 focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Nouveau mot de passe" autoFocus />
            <div className="flex gap-3">
              <button onClick={onClose} className="flex-1 py-2.5 border rounded-xl hover:bg-gray-50">Annuler</button>
              <button onClick={handleReset} disabled={loading}
                className="flex-1 py-2.5 bg-red-600 text-white rounded-xl hover:bg-red-700 disabled:opacity-50 flex items-center justify-center gap-2">
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Key className="w-4 h-4" />} Reset
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

// ─── Main Dashboard ──────────────────────────────────────────

type Tab = 'overview' | 'users' | 'promoCodes' | 'inscriptions' | 'usage' | 'requests';

interface RegistrationRequest {
  id: string;
  nom: string;
  prenom: string;
  phone: string;
  ville: string;
  email?: string | null;
  niveau?: string | null;
  promo_code?: string | null;
  message?: string | null;
  status: string;
  admin_notes?: string | null;
  contacted_at?: string | null;
  activated_at?: string | null;
  created_user_id?: string | null;
  created_at: string;
  updated_at: string;
}

export default function AdminDashboard() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('admin_token'));
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const [dataLoading, setDataLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Data
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [users, setUsers] = useState<UserRecord[]>([]);
  const [usageSummary, setUsageSummary] = useState<UsageSummary | null>(null);
  const [userUsage, setUserUsage] = useState<UserUsage[]>([]);
  const [recentReqs, setRecentReqs] = useState<RecentRequest[]>([]);
  const [onlineInfo, setOnlineInfo] = useState<{ online_count: number; online_users: any[] }>({ online_count: 0, online_users: [] });

  // UI state
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [resetPwUser, setResetPwUser] = useState<{ id: string; name: string } | null>(null);
  const [usageDays, setUsageDays] = useState(30);
  const [filterPromoCode, setFilterPromoCode] = useState<string>('');
  const [filterAccountType, setFilterAccountType] = useState<'all' | 'permanent' | 'test' | 'expired' | 'admin'>('all');
  const [filterStatus, setFilterStatus] = useState<'all' | 'active' | 'inactive' | 'online'>('all');
  const [promoPeriod, setPromoPeriod] = useState<'all' | '7d' | '30d' | '90d' | 'month'>('all');
  const [promoMonth, setPromoMonth] = useState<string>(() => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
  });
  const [promoType, setPromoType] = useState<'all' | 'permanent' | 'test' | 'expired'>('all');
  const [expandedUser, setExpandedUser] = useState<string | null>(null);
  const [selectedUserIds, setSelectedUserIds] = useState<Set<string>>(new Set());
  const [bulkLoading, setBulkLoading] = useState(false);

  const loadData = useCallback(async () => {
    if (!localStorage.getItem('admin_token')) return;
    setDataLoading(true);
    try {
      const [dashRes, usersRes, onlineRes] = await Promise.all([
        getAdminDashboard(),
        getAdminUsers(),
        getOnlineUsers(),
      ]);
      setStats(dashRes.data);
      setUsers(usersRes.data.users || []);
      setOnlineInfo(onlineRes.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        localStorage.removeItem('admin_token');
        setIsLoggedIn(false);
      }
    } finally {
      setDataLoading(false);
    }
  }, []);

  const loadUsageData = useCallback(async () => {
    if (!localStorage.getItem('admin_token')) return;
    try {
      const [summaryRes, byUserRes, recentRes] = await Promise.all([
        getUsageSummary(usageDays),
        getUsageByUser(usageDays),
        getRecentRequests(100),
      ]);
      setUsageSummary(summaryRes.data);
      setUserUsage(byUserRes.data.users || []);
      setRecentReqs(recentRes.data.requests || []);
    } catch (err) {
      console.error('Failed to load usage data:', err);
    }
  }, [usageDays]);

  useEffect(() => {
    if (isLoggedIn) {
      loadData();
      loadUsageData();
    }
  }, [isLoggedIn, loadData, loadUsageData]);

  // Auto-refresh every 30s
  useEffect(() => {
    if (!isLoggedIn || !autoRefresh) return;
    const interval = setInterval(() => {
      loadData();
      if (activeTab === 'usage' || activeTab === 'requests') loadUsageData();
    }, 30000);
    return () => clearInterval(interval);
  }, [isLoggedIn, autoRefresh, activeTab, loadData, loadUsageData]);

  // Listen to global 401 events from any admin API call
  useEffect(() => {
    const onUnauthorized = () => setIsLoggedIn(false);
    window.addEventListener('admin:unauthorized', onUnauthorized);
    return () => window.removeEventListener('admin:unauthorized', onUnauthorized);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setIsLoggedIn(false);
  };

  const handleToggleActive = async (userId: string, currentActive: boolean) => {
    try {
      await updateAdminUser(userId, { is_active: !currentActive });
      loadData();
    } catch (err) {
      console.error('Failed to toggle user:', err);
    }
  };

  const handleDeleteUser = async (userId: string) => {
    if (!confirm('Désactiver cet utilisateur?')) return;
    try {
      await deleteAdminUser(userId);
      loadData();
    } catch (err: any) {
      console.error('Failed to delete user:', err);
      if (err?.response?.status === 401) {
        alert('Session expirée. Veuillez vous reconnecter.');
      } else {
        alert('Échec de la suppression: ' + (err?.response?.data?.detail || err?.message || 'erreur inconnue'));
      }
    }
  };

  const toggleSelectUser = (id: string) => {
    setSelectedUserIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selectedUserIds.size === filteredUsers.length) {
      setSelectedUserIds(new Set());
    } else {
      setSelectedUserIds(new Set(filteredUsers.map(u => u.id)));
    }
  };

  const handleBulkAction = async (action: 'delete' | 'activate' | 'deactivate') => {
    const ids = Array.from(selectedUserIds);
    const labels: Record<string, string> = {
      delete: `Supprimer ${ids.length} compte(s) ?`,
      activate: `Activer ${ids.length} compte(s) ?`,
      deactivate: `Désactiver ${ids.length} compte(s) ?`,
    };
    if (!confirm(labels[action])) return;
    setBulkLoading(true);
    try {
      await bulkUserAction(ids, action);
      setSelectedUserIds(new Set());
      loadData();
    } catch (err: any) {
      console.error('Bulk action failed:', err);
      if (err?.response?.status === 401) {
        alert('Session expirée. Veuillez vous reconnecter.');
      } else {
        alert('Échec de l\'action groupée: ' + (err?.response?.data?.detail || err?.message || 'erreur inconnue'));
      }
    } finally {
      setBulkLoading(false);
    }
  };

  if (!isLoggedIn) {
    return <AdminLoginScreen onLogin={() => setIsLoggedIn(true)} />;
  }

  const now = Date.now();
  const getAccountType = (u: UserRecord): 'admin' | 'expired' | 'test' | 'permanent' => {
    if (u.is_admin) return 'admin';
    if (u.expires_at) {
      return new Date(u.expires_at).getTime() < now ? 'expired' : 'test';
    }
    return 'permanent';
  };

  const matchesSearch = (u: UserRecord) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      u.email?.toLowerCase().includes(q) ||
      u.full_name?.toLowerCase().includes(q) ||
      u.username?.toLowerCase().includes(q) ||
      u.promo_code?.toLowerCase().includes(q)
    );
  };

  const filteredUsers = users.filter(u => {
    if (!matchesSearch(u)) return false;
    if (filterPromoCode && (u.promo_code || '').toUpperCase() !== filterPromoCode.toUpperCase()) return false;
    if (filterAccountType !== 'all' && getAccountType(u) !== filterAccountType) return false;
    if (filterStatus === 'active' && !u.is_active) return false;
    if (filterStatus === 'inactive' && u.is_active) return false;
    if (filterStatus === 'online' && !u.is_online) return false;
    return true;
  });

  // Promo code stats: time-window filter on created_at
  const promoFilterRange = (() => {
    if (promoPeriod === 'all') return null;
    if (promoPeriod === 'month') {
      const [y, m] = promoMonth.split('-').map(Number);
      const start = new Date(y, m - 1, 1).getTime();
      const end = new Date(y, m, 1).getTime();
      return { start, end };
    }
    const days = promoPeriod === '7d' ? 7 : promoPeriod === '30d' ? 30 : 90;
    return { start: now - days * 86400000, end: now + 86400000 };
  })();

  const usersInPromoWindow = (promoFilterRange
    ? users.filter(u => {
        if (!u.created_at) return false;
        const t = new Date(u.created_at).getTime();
        return t >= promoFilterRange.start && t < promoFilterRange.end;
      })
    : users
  ).filter(u => {
    if (promoType === 'all') return true;
    return getAccountType(u) === promoType;
  });

  const promoStats = usersInPromoWindow.reduce<Record<string, { total: number; active: number; online: number; test: number; permanent: number }>>((acc, u) => {
    const code = u.promo_code || '(sans code)';
    if (!acc[code]) acc[code] = { total: 0, active: 0, online: 0, test: 0, permanent: 0 };
    acc[code].total += 1;
    if (u.is_active) acc[code].active += 1;
    if (u.is_online) acc[code].online += 1;
    const t = getAccountType(u);
    if (t === 'test') acc[code].test += 1;
    if (t === 'permanent') acc[code].permanent += 1;
    return acc;
  }, {});
  const promoCodesList = Object.keys(promoStats)
    .filter(c => c !== '(sans code)')
    .sort();

  // Aggregate counts (filtered users)
  const counts = {
    total: filteredUsers.length,
    active: filteredUsers.filter(u => u.is_active).length,
    online: filteredUsers.filter(u => u.is_online).length,
    test: filteredUsers.filter(u => getAccountType(u) === 'test').length,
    permanent: filteredUsers.filter(u => getAccountType(u) === 'permanent').length,
    expired: filteredUsers.filter(u => getAccountType(u) === 'expired').length,
    admin: filteredUsers.filter(u => getAccountType(u) === 'admin').length,
  };

  const tabs: { key: Tab; label: string; icon: any }[] = [
    { key: 'overview', label: 'Vue d\'ensemble', icon: BarChart3 },
    { key: 'users', label: 'Utilisateurs', icon: Users },
    { key: 'promoCodes', label: 'Codes promo', icon: Key },
    { key: 'inscriptions', label: 'Inscriptions', icon: Inbox },
    { key: 'usage', label: 'Consommation', icon: DollarSign },
    { key: 'requests', label: 'Requêtes récentes', icon: Activity },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-[1800px] mx-auto px-3 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14 sm:h-16 gap-2">
            <div className="flex items-center gap-2 sm:gap-3 min-w-0">
              <div className="p-1.5 sm:p-2 bg-red-600 rounded-lg sm:rounded-xl flex-shrink-0">
                <Shield className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
              </div>
              <div className="min-w-0">
                <h1 className="text-sm sm:text-lg font-bold text-gray-900 truncate">Admin Dashboard</h1>
                <p className="text-[10px] sm:text-xs text-gray-500 font-brand">معلم</p>
              </div>
            </div>
            <div className="flex items-center gap-1 sm:gap-3 flex-shrink-0">
              {/* Online indicator (icon only on mobile) */}
              <div className="flex items-center gap-1.5 px-2 sm:px-3 py-1 sm:py-1.5 bg-green-50 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-xs sm:text-sm font-medium text-green-700">
                  {onlineInfo.online_count}<span className="hidden sm:inline"> en ligne</span>
                </span>
              </div>
              {/* Auto refresh */}
              <button onClick={() => setAutoRefresh(!autoRefresh)}
                className={`p-1.5 sm:p-2 rounded-lg transition-colors ${autoRefresh ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-400'}`}
                title={autoRefresh ? 'Auto-refresh ON' : 'Auto-refresh OFF'}>
                <RefreshCw className={`w-4 h-4 ${autoRefresh ? 'animate-spin' : ''}`} style={autoRefresh ? { animationDuration: '3s' } : {}} />
              </button>
              {/* Manual refresh */}
              <button onClick={() => { loadData(); loadUsageData(); }}
                className={`p-1.5 sm:p-2 hover:bg-gray-100 rounded-lg ${dataLoading ? 'animate-pulse' : ''}`} title="Rafraîchir">
                <RefreshCw className={`w-4 h-4 ${dataLoading ? 'animate-spin' : ''}`} />
              </button>
              {/* Exam Extractor link */}
              <a href="/admin/exam-extractor"
                title="Extraire PDF"
                className="flex items-center gap-1.5 p-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm text-purple-600 hover:bg-purple-50 rounded-lg">
                <FileUp className="w-4 h-4" /> <span className="hidden md:inline">Extraire PDF</span>
              </a>
              <button onClick={handleLogout}
                title="Déconnexion"
                className="flex items-center gap-1.5 p-1.5 sm:px-3 sm:py-2 text-xs sm:text-sm text-red-600 hover:bg-red-50 rounded-lg">
                <LogOut className="w-4 h-4" /> <span className="hidden md:inline">Déconnexion</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-[1800px] mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6">
        {/* Tabs — horizontally scrollable on mobile, equal-width from sm+ */}
        <div className="flex gap-1 bg-white rounded-xl p-1 shadow-sm border mb-4 sm:mb-6 overflow-x-auto">
          {tabs.map(t => (
            <button key={t.key} onClick={() => { setActiveTab(t.key); if (t.key === 'usage' || t.key === 'requests') loadUsageData(); }}
              className={`sm:flex-1 flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg text-xs sm:text-sm font-medium transition-all flex-shrink-0 whitespace-nowrap ${
                activeTab === t.key ? 'bg-gray-900 text-white shadow-sm' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}>
              <t.icon className="w-4 h-4 flex-shrink-0" /> <span>{t.label}</span>
            </button>
          ))}
        </div>

        {/* ──── OVERVIEW TAB ──── */}
        {activeTab === 'overview' && stats && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatCard icon={Users} label="Utilisateurs" value={stats.total_users}
                sub={`${stats.active_users} actifs`} color="bg-blue-500" />
              <StatCard icon={Wifi} label="En ligne" value={stats.online_count}
                sub="Connectés maintenant" color="bg-green-500" />
              <StatCard icon={DollarSign} label="Coût aujourd'hui" value={`$${stats.today.cost_usd.toFixed(4)}`}
                sub={`${stats.today.requests} requêtes`} color="bg-amber-500" />
              <StatCard icon={TrendingUp} label="Coût ce mois" value={`$${stats.this_month.cost_usd.toFixed(4)}`}
                sub={`Total: $${stats.all_time_cost_usd.toFixed(4)}`} color="bg-red-500" />
            </div>

            {/* Today details */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-2xl p-6 shadow-sm border">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-500" /> Activité du jour
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-50">
                    <span className="text-gray-600">Requêtes API</span>
                    <span className="font-bold text-gray-900">{stats.today.requests}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-50">
                    <span className="text-gray-600">Tokens utilisés</span>
                    <span className="font-bold text-gray-900">{stats.today.tokens.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-50">
                    <span className="text-gray-600">Coût</span>
                    <span className="font-bold text-green-600">${stats.today.cost_usd.toFixed(4)}</span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">Tokens ce mois</span>
                    <span className="font-bold text-gray-900">{stats.this_month.tokens.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              {/* Online users */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <Wifi className="w-5 h-5 text-green-500" /> Utilisateurs en ligne ({onlineInfo.online_count})
                </h3>
                {onlineInfo.online_users.length === 0 ? (
                  <p className="text-gray-400 text-sm py-4 text-center">Aucun utilisateur connecté</p>
                ) : (
                  <div className="space-y-2 max-h-80 overflow-y-auto">
                    {onlineInfo.online_users.map((u, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 bg-green-50 rounded-xl">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900">{u.full_name || u.username}</p>
                          <p className="text-xs text-gray-500 truncate">{u.email}</p>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <p className="text-xs font-mono text-gray-600">{u.ip || '-'}</p>
                          {u.connected_at && (
                            <p className="text-[10px] text-gray-400">
                              {new Date(u.connected_at + 'Z').toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ──── USERS TAB ──── */}
        {activeTab === 'users' && (
          <div className="space-y-4">
            {/* Mini dashboard cards */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
              <StatCard icon={Users} label="Total" value={counts.total} sub="utilisateurs" color="bg-blue-500" />
              <StatCard icon={Check} label="Actifs" value={counts.active} sub={`${counts.total - counts.active} inactifs`} color="bg-green-500" />
              <StatCard icon={Wifi} label="En ligne" value={counts.online} sub="connectés" color="bg-emerald-500" />
              <StatCard icon={Lock} label="Permanents" value={counts.permanent} sub="comptes" color="bg-indigo-500" />
              <StatCard icon={Clock} label="Tests" value={counts.test} sub={`${counts.expired} expirés`} color="bg-amber-500" />
              <StatCard icon={Shield} label="Admins" value={counts.admin} sub="comptes" color="bg-red-500" />
            </div>

            {/* Promo code stats */}
            {users.length > 0 && (
              <div className="bg-white rounded-2xl p-5 shadow-sm border">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-2 mb-4">
                  <h3 className="font-bold text-gray-900 flex items-center gap-1.5 mr-auto whitespace-nowrap">
                    <Key className="w-4 h-4 text-indigo-600" /> Codes promo
                    <span className="text-[11px] font-normal text-gray-400">({usersInPromoWindow.length})</span>
                  </h3>
                  <div className="inline-flex items-center bg-gray-100 rounded-lg p-0.5">
                    {([
                      { key: 'all', label: 'Tout' },
                      { key: '7d', label: '7j' },
                      { key: '30d', label: '30j' },
                      { key: '90d', label: '90j' },
                      { key: 'month', label: 'Mois' },
                    ] as const).map(p => (
                      <button key={p.key} onClick={() => setPromoPeriod(p.key)}
                        className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors whitespace-nowrap ${
                          promoPeriod === p.key ? 'bg-indigo-600 text-white shadow-sm' : 'text-gray-600 hover:bg-white'
                        }`}>
                        {p.label}
                      </button>
                    ))}
                  </div>
                  {promoPeriod === 'month' && (
                    <input type="month" value={promoMonth} onChange={e => setPromoMonth(e.target.value)}
                      className="px-2 py-1 border rounded-md text-[11px] focus:ring-2 focus:ring-indigo-500 outline-none" />
                  )}
                  <div className="inline-flex items-center bg-gray-100 rounded-lg p-0.5">
                    {([
                      { key: 'all', label: 'Tous' },
                      { key: 'permanent', label: 'Perm.' },
                      { key: 'test', label: 'Test' },
                      { key: 'expired', label: 'Exp.' },
                    ] as const).map(t => (
                      <button key={t.key} onClick={() => setPromoType(t.key)}
                        className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors whitespace-nowrap ${
                          promoType === t.key ? 'bg-amber-600 text-white shadow-sm' : 'text-gray-600 hover:bg-white'
                        }`}>
                        {t.label}
                      </button>
                    ))}
                  </div>
                </div>
                {Object.keys(promoStats).length === 0 && (
                  <div className="text-center py-8 text-sm text-gray-400">
                    Aucun utilisateur ne correspond aux filtres sélectionnés
                  </div>
                )}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {Object.entries(promoStats)
                    .sort((a, b) => b[1].total - a[1].total)
                    .map(([code, s]) => (
                      <button key={code}
                        onClick={() => {
                          if (code === '(sans code)') {
                            setFilterPromoCode('');
                          } else {
                            setFilterPromoCode(filterPromoCode === code ? '' : code);
                          }
                        }}
                        className={`text-left p-3 rounded-xl border transition-all ${
                          filterPromoCode === code
                            ? 'border-indigo-500 bg-indigo-50'
                            : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
                        } ${code === '(sans code)' ? 'opacity-80' : ''}`}>
                        <div className="flex items-center justify-between mb-2">
                          <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                            code === '(sans code)' ? 'bg-gray-100 text-gray-600' : 'bg-indigo-100 text-indigo-700'
                          }`}>{code}</span>
                          <span className="text-2xl font-bold text-gray-900">{s.total}</span>
                        </div>
                        <div className="flex flex-wrap gap-2 text-[11px] text-gray-500">
                          <span><span className="font-semibold text-green-600">{s.active}</span> actifs</span>
                          <span>•</span>
                          <span><span className="font-semibold text-emerald-600">{s.online}</span> en ligne</span>
                          <span>•</span>
                          <span><span className="font-semibold text-indigo-600">{s.permanent}</span> perm.</span>
                          <span>•</span>
                          <span><span className="font-semibold text-amber-600">{s.test}</span> test</span>
                        </div>
                      </button>
                  ))}
                </div>
              </div>
            )}

            {/* Search + filters row */}
            <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input type="text" value={searchQuery} onChange={e => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-white border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                  placeholder="Rechercher par nom, email, username, code promo..." />
              </div>
              <select value={filterPromoCode} onChange={e => setFilterPromoCode(e.target.value)}
                className="px-3 py-2.5 bg-white border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="">Tous les codes promo</option>
                {promoCodesList.map(code => (
                  <option key={code} value={code}>{code}</option>
                ))}
              </select>
              <select value={filterAccountType} onChange={e => setFilterAccountType(e.target.value as any)}
                className="px-3 py-2.5 bg-white border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="all">Tous types</option>
                <option value="permanent">Permanent</option>
                <option value="test">Test (24h)</option>
                <option value="expired">Expiré</option>
                <option value="admin">Admin</option>
              </select>
              <select value={filterStatus} onChange={e => setFilterStatus(e.target.value as any)}
                className="px-3 py-2.5 bg-white border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="all">Tous statuts</option>
                <option value="active">Actifs</option>
                <option value="inactive">Inactifs</option>
                <option value="online">En ligne</option>
              </select>
              {(filterPromoCode || filterAccountType !== 'all' || filterStatus !== 'all' || searchQuery) && (
                <button onClick={() => { setFilterPromoCode(''); setFilterAccountType('all'); setFilterStatus('all'); setSearchQuery(''); setSelectedUserIds(new Set()); }}
                  className="flex items-center gap-1 px-3 py-2.5 text-sm text-gray-600 border rounded-xl hover:bg-gray-50">
                  <X className="w-4 h-4" /> Réinitialiser
                </button>
              )}
              <button onClick={() => setShowCreateModal(true)}
                className="flex items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 font-medium">
                <Plus className="w-4 h-4" /> Créer un compte
              </button>
            </div>

            {/* ── Bulk action bar ── */}
            {selectedUserIds.size > 0 && (
              <div className="flex items-center gap-3 px-4 py-3 bg-indigo-50 border border-indigo-200 rounded-xl animate-in fade-in">
                <span className="text-sm font-semibold text-indigo-800">
                  {selectedUserIds.size} sélectionné{selectedUserIds.size > 1 ? 's' : ''}
                </span>
                <div className="flex-1" />
                <button onClick={() => handleBulkAction('activate')} disabled={bulkLoading}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors">
                  <Check className="w-3.5 h-3.5" /> Activer
                </button>
                <button onClick={() => handleBulkAction('deactivate')} disabled={bulkLoading}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium bg-amber-600 text-white rounded-lg hover:bg-amber-700 disabled:opacity-50 transition-colors">
                  <X className="w-3.5 h-3.5" /> Désactiver
                </button>
                <button onClick={() => handleBulkAction('delete')} disabled={bulkLoading}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors">
                  <Trash2 className="w-3.5 h-3.5" /> Supprimer
                </button>
                <button onClick={() => setSelectedUserIds(new Set())}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 border border-gray-300 rounded-lg hover:bg-white transition-colors">
                  Désélectionner
                </button>
              </div>
            )}

            <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-50 border-b">
                      <th className="w-10 px-3 py-3">
                        <input type="checkbox"
                          checked={filteredUsers.length > 0 && selectedUserIds.size === filteredUsers.length}
                          onChange={toggleSelectAll}
                          className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer" />
                      </th>
                      <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Utilisateur</th>
                      <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Email</th>
                      <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Code promo</th>
                      <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Type</th>
                      <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Statut</th>
                      <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Rôle</th>
                      <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">En ligne</th>
                      <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Inscrit le</th>
                      <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {filteredUsers.map(u => (
                      <tr key={u.id} className={`hover:bg-gray-50 transition-colors ${selectedUserIds.has(u.id) ? 'bg-indigo-50/50' : ''}`}>
                        <td className="w-10 px-3 py-3">
                          <input type="checkbox"
                            checked={selectedUserIds.has(u.id)}
                            onChange={() => toggleSelectUser(u.id)}
                            className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer" />
                        </td>
                        <td className="px-4 py-3">
                          <div>
                            <p className="font-medium text-gray-900 text-sm">{u.full_name}</p>
                            <p className="text-xs text-gray-400">@{u.username}</p>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-600">{u.email}</td>
                        <td className="px-4 py-3 text-sm">
                          {u.promo_code ? (
                            <span className="px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 font-semibold text-xs">{u.promo_code}</span>
                          ) : (
                            <span className="text-gray-300">-</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-center">
                          {(() => {
                            const t = getAccountType(u);
                            const styles: Record<string, string> = {
                              admin: 'bg-red-100 text-red-700',
                              permanent: 'bg-indigo-100 text-indigo-700',
                              test: 'bg-amber-100 text-amber-700',
                              expired: 'bg-gray-200 text-gray-500',
                            };
                            const labels: Record<string, string> = {
                              admin: 'Admin',
                              permanent: 'Permanent',
                              test: 'Test',
                              expired: 'Expiré',
                            };
                            return (
                              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${styles[t]}`}
                                title={u.expires_at ? `Expire: ${new Date(u.expires_at).toLocaleString('fr-FR')}` : ''}>
                                {labels[t]}
                              </span>
                            );
                          })()}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <button onClick={() => handleToggleActive(u.id, u.is_active)}
                            className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                              u.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                            }`}>
                            {u.is_active ? 'Actif' : 'Inactif'}
                          </button>
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                            u.is_admin ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'
                          }`}>
                            {u.is_admin ? 'Admin' : 'Élève'}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center">
                          {u.is_online ? (() => {
                            const info = onlineInfo.online_users.find((o: any) => o.id === u.id);
                            return (
                              <div className="inline-flex flex-col items-center gap-0.5">
                                <Wifi className="w-4 h-4 text-green-500" />
                                {info?.ip && <span className="text-[10px] font-mono text-gray-500 leading-none">{info.ip}</span>}
                              </div>
                            );
                          })() : (
                            <WifiOff className="w-4 h-4 text-gray-300 mx-auto" />
                          )}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">
                          {u.created_at ? new Date(u.created_at).toLocaleDateString('fr-FR') : '-'}
                        </td>
                        <td className="px-4 py-3 text-right">
                          <div className="flex items-center justify-end gap-1">
                            <button onClick={() => setResetPwUser({ id: u.id, name: u.full_name || u.username })}
                              className="p-2 hover:bg-blue-50 rounded-lg text-blue-600" title="Réinitialiser le mot de passe">
                              <Key className="w-4 h-4" />
                            </button>
                            <button onClick={() => handleDeleteUser(u.id)}
                              className="p-2 hover:bg-red-50 rounded-lg text-red-600" title="Désactiver">
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {filteredUsers.length === 0 && (
                <div className="text-center py-8 text-gray-400">Aucun utilisateur trouvé</div>
              )}
            </div>
          </div>
        )}

        {/* ──── USAGE TAB ──── */}
        {activeTab === 'usage' && (
          <div className="space-y-6">
            {/* Period selector */}
            <div className="flex items-center gap-2">
              {[7, 14, 30, 90].map(d => (
                <button key={d} onClick={() => setUsageDays(d)}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                    usageDays === d ? 'bg-gray-900 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'
                  }`}>
                  {d} jours
                </button>
              ))}
            </div>

            {usageSummary && (
              <>
                {/* Summary cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <StatCard icon={DollarSign} label={`Coût (${usageDays}j)`}
                    value={`$${usageSummary.total_cost_usd.toFixed(4)}`}
                    sub={`${usageSummary.total_requests} requêtes`} color="bg-green-500" />
                  <StatCard icon={Zap} label="Tokens totaux"
                    value={usageSummary.total_tokens.toLocaleString()}
                    sub={`Prompt: ${usageSummary.total_prompt_tokens.toLocaleString()}`} color="bg-blue-500" />
                  <StatCard icon={Server} label="Requêtes"
                    value={usageSummary.total_requests}
                    sub={`Completion: ${usageSummary.total_completion_tokens.toLocaleString()}`} color="bg-purple-500" />
                  <StatCard icon={Activity} label="Providers"
                    value={Object.keys(usageSummary.providers).length}
                    sub="Services utilisés" color="bg-amber-500" />
                </div>

                {/* Provider breakdown */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white rounded-2xl p-6 shadow-sm border">
                    <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <Server className="w-5 h-5 text-purple-500" /> Par fournisseur
                    </h3>
                    <div className="space-y-3">
                      {Object.entries(usageSummary.providers).map(([provider, data]) => {
                        const pct = usageSummary.total_cost_usd > 0
                          ? (data.cost_usd / usageSummary.total_cost_usd * 100)
                          : 0;
                        return (
                          <div key={provider} className="space-y-1">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <ProviderBadge provider={provider} />
                                <span className="text-sm text-gray-600">{data.requests} req</span>
                              </div>
                              <span className="text-sm font-bold text-gray-900">${data.cost_usd.toFixed(4)}</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2">
                              <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all"
                                style={{ width: `${Math.max(pct, 2)}%` }} />
                            </div>
                            <p className="text-xs text-gray-400">{data.tokens.toLocaleString()} tokens | {pct.toFixed(1)}% du coût</p>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Daily chart (simple bar representation) */}
                  <div className="bg-white rounded-2xl p-6 shadow-sm border">
                    <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <BarChart3 className="w-5 h-5 text-blue-500" /> Coût par jour (derniers 14j)
                    </h3>
                    <div className="space-y-1.5">
                      {Object.entries(usageSummary.daily)
                        .sort(([a], [b]) => b.localeCompare(a))
                        .slice(0, 14)
                        .reverse()
                        .map(([day, data]) => {
                          const maxCost = Math.max(...Object.values(usageSummary.daily).map(d => d.cost_usd), 0.001);
                          const pct = (data.cost_usd / maxCost) * 100;
                          return (
                            <div key={day} className="flex items-center gap-2">
                              <span className="text-xs text-gray-400 w-12 shrink-0">{day.slice(5)}</span>
                              <div className="flex-1 bg-gray-100 rounded-full h-5 relative">
                                <div className="bg-gradient-to-r from-blue-400 to-blue-600 h-5 rounded-full transition-all flex items-center justify-end pr-2"
                                  style={{ width: `${Math.max(pct, 3)}%` }}>
                                  {pct > 20 && <span className="text-[10px] text-white font-medium">${data.cost_usd.toFixed(4)}</span>}
                                </div>
                              </div>
                              <span className="text-xs text-gray-500 w-10 text-right">{data.requests}r</span>
                            </div>
                          );
                        })}
                    </div>
                  </div>
                </div>

                {/* Usage by user */}
                <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
                  <div className="p-6 border-b">
                    <h3 className="font-bold text-gray-900 flex items-center gap-2">
                      <Users className="w-5 h-5 text-blue-500" /> Consommation par utilisateur
                    </h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="bg-gray-50 border-b">
                          <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Utilisateur</th>
                          <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Requêtes</th>
                          <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Tokens</th>
                          <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Coût ($)</th>
                          <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Dernière req.</th>
                          <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Détails</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-50">
                        {userUsage.map(u => (
                          <>
                            <tr key={u.student_id} className="hover:bg-gray-50">
                              <td className="px-4 py-3 text-sm">
                                <div>
                                  <p className="font-medium text-gray-900">
                                    {u.full_name || u.username || u.student_email || 'Anonyme'}
                                  </p>
                                  {u.student_email && (
                                    <p className="text-xs text-gray-400">{u.student_email}</p>
                                  )}
                                </div>
                              </td>
                              <td className="px-4 py-3 text-sm text-right font-mono">{u.requests}</td>
                              <td className="px-4 py-3 text-sm text-right font-mono">{u.total_tokens.toLocaleString()}</td>
                              <td className="px-4 py-3 text-sm text-right font-mono font-bold text-green-600">
                                ${u.cost_usd.toFixed(4)}
                              </td>
                              <td className="px-4 py-3 text-xs text-right text-gray-400">
                                {u.last_request ? new Date(u.last_request).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : '-'}
                              </td>
                              <td className="px-4 py-3 text-center">
                                <button onClick={() => setExpandedUser(expandedUser === u.student_id ? null : u.student_id)}
                                  className="p-1 hover:bg-gray-100 rounded">
                                  {expandedUser === u.student_id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                                </button>
                              </td>
                            </tr>
                            {expandedUser === u.student_id && (
                              <tr key={`${u.student_id}-detail`}>
                                <td colSpan={6} className="px-4 py-3 bg-gray-50">
                                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                                    {Object.entries(u.providers).map(([p, data]) => (
                                      <div key={p} className="bg-white rounded-xl p-3 border">
                                        <ProviderBadge provider={p} />
                                        <div className="mt-2 space-y-1">
                                          <p className="text-xs text-gray-500">{data.requests} requêtes</p>
                                          <p className="text-xs text-gray-500">{data.tokens.toLocaleString()} tokens</p>
                                          <p className="text-sm font-bold text-gray-900">${data.cost_usd.toFixed(4)}</p>
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                  <div className="mt-2 text-xs text-gray-400">
                                    Prompt: {u.prompt_tokens.toLocaleString()} | Completion: {u.completion_tokens.toLocaleString()}
                                  </div>
                                </td>
                              </tr>
                            )}
                          </>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {userUsage.length === 0 && (
                    <div className="text-center py-8 text-gray-400">Aucune donnée de consommation</div>
                  )}
                </div>
              </>
            )}
          </div>
        )}

        {/* ──── REQUESTS TAB ──── */}
        {activeTab === 'requests' && (
          <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
            <div className="p-6 border-b flex items-center justify-between">
              <h3 className="font-bold text-gray-900 flex items-center gap-2">
                <Clock className="w-5 h-5 text-blue-500" /> Requêtes récentes (100 dernières)
              </h3>
              <button onClick={loadUsageData}
                className="flex items-center gap-1 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg">
                <RefreshCw className="w-3 h-3" /> Refresh
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50 border-b">
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Heure</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Utilisateur</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Provider</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Model</th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Endpoint</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Tokens</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Coût</th>
                    <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Durée</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {recentReqs.map((r, i) => (
                    <tr key={r.id || i} className="hover:bg-gray-50 text-sm">
                      <td className="px-4 py-2.5 text-xs text-gray-500">
                        {r.created_at ? new Date(r.created_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'medium' }) : '-'}
                      </td>
                      <td className="px-4 py-2.5 text-gray-600 max-w-[150px] truncate">{r.student_email || '-'}</td>
                      <td className="px-4 py-2.5"><ProviderBadge provider={r.provider} /></td>
                      <td className="px-4 py-2.5 text-xs text-gray-500 font-mono">{r.model}</td>
                      <td className="px-4 py-2.5">
                        <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{r.endpoint}</span>
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono text-xs">
                        {r.total_tokens.toLocaleString()}
                        <span className="text-gray-400 ml-1">({r.prompt_tokens}+{r.completion_tokens})</span>
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono text-xs font-bold text-green-600">
                        ${Number(r.cost_usd).toFixed(6)}
                      </td>
                      <td className="px-4 py-2.5 text-right text-xs text-gray-400">
                        {r.request_duration_ms ? `${(r.request_duration_ms / 1000).toFixed(1)}s` : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {recentReqs.length === 0 && (
              <div className="text-center py-8 text-gray-400">Aucune requête enregistrée</div>
            )}
          </div>
        )}

        {/* ──── PROMO CODES TAB ──── */}
        {activeTab === 'promoCodes' && <PromoCodesTab />}

        {/* ──── INSCRIPTIONS TAB ──── */}
        {activeTab === 'inscriptions' && <RegistrationRequestsTab />}
      </div>

      {/* Modals */}
      {showCreateModal && <CreateUserModal onClose={() => setShowCreateModal(false)} onCreated={loadData} />}
      {resetPwUser && <ResetPasswordModal userId={resetPwUser.id} userName={resetPwUser.name} onClose={() => setResetPwUser(null)} />}
    </div>
  );
}

interface PromoCodeRecord {
  id: string;
  code: string;
  label?: string | null;
  is_active: boolean;
  created_at?: string | null;
}

function PromoCodesTab() {
  const [items, setItems] = useState<PromoCodeRecord[]>([]);
  const [form, setForm] = useState({ code: '', label: '' });
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const getErrorMessage = (err: any, fallback: string) => {
    const detail = err?.response?.data?.detail;
    if (typeof detail === 'string') return detail;
    if (detail) return JSON.stringify(detail);
    return err?.message || fallback;
  };

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await listPromoCodes();
      setItems(res.data.promo_codes || []);
    } catch (err: any) {
      setError(getErrorMessage(err, 'Erreur de chargement'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const code = form.code.trim().toUpperCase();
    if (!code) {
      setError('Code promo obligatoire');
      return;
    }
    setSaving(true);
    try {
      await createPromoCode({ code, label: form.label.trim() || undefined, is_active: true });
      setForm({ code: '', label: '' });
      load();
    } catch (err: any) {
      setError(getErrorMessage(err, 'Erreur lors de la création'));
    } finally {
      setSaving(false);
    }
  };

  const toggleActive = async (item: PromoCodeRecord) => {
    try {
      await updatePromoCode(item.id, { is_active: !item.is_active });
      load();
    } catch (err: any) {
      setError(getErrorMessage(err, 'Erreur lors de la modification'));
    }
  };

  const remove = async (id: string) => {
    if (!confirm('Supprimer ce code promo ?')) return;
    try {
      await deletePromoCode(id);
      load();
    } catch (err: any) {
      setError(getErrorMessage(err, 'Erreur lors de la suppression'));
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-2xl p-5 shadow-sm border">
        <h3 className="font-bold text-gray-900 flex items-center gap-2 mb-4">
          <Key className="w-5 h-5 text-indigo-600" /> Créer un code promo
        </h3>
        {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{error}</div>}
        <form onSubmit={handleCreate} className="grid md:grid-cols-[1fr_1fr_auto] gap-3">
          <input
            value={form.code}
            onChange={e => setForm({ ...form, code: e.target.value.toUpperCase() })}
            className="px-4 py-2.5 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none uppercase"
            placeholder="Code promo ex: ECOLE123"
          />
          <input
            value={form.label}
            onChange={e => setForm({ ...form, label: e.target.value })}
            className="px-4 py-2.5 border rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none"
            placeholder="Source / description ex: Lycée Al Farabi"
          />
          <button
            type="submit"
            disabled={saving}
            className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 flex items-center justify-center gap-2 font-semibold"
          >
            {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            Créer
          </button>
        </form>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
        <div className="flex items-center justify-between p-5 border-b">
          <h3 className="font-bold text-gray-900">Codes promo créés ({items.length})</h3>
          <button onClick={load} className="flex items-center gap-2 px-3 py-2 text-sm border rounded-lg hover:bg-gray-50">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Actualiser
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Code</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Source</th>
                <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Statut</th>
                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Créé le</th>
                <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {items.map(item => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <span className="px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 font-bold text-xs">{item.code}</span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">{item.label || '-'}</td>
                  <td className="px-4 py-3 text-center">
                    <button onClick={() => toggleActive(item)}
                      className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                        item.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                      }`}>
                      {item.is_active ? 'Actif' : 'Désactivé'}
                    </button>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {item.created_at ? new Date(item.created_at).toLocaleDateString('fr-FR') : '-'}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button onClick={() => remove(item.id)} className="p-2 hover:bg-red-50 rounded-lg text-red-600">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {items.length === 0 && (
          <div className="text-center py-10 text-gray-400">Aucun code promo créé</div>
        )}
      </div>
    </div>
  );
}

// ─── Registration Requests Tab ───────────────────────────────

function RegistrationRequestsTab() {
  const [items, setItems] = useState<RegistrationRequest[]>([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<string>('');
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [activateTarget, setActivateTarget] = useState<RegistrationRequest | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await listRegistrationRequests(filter || undefined);
      setItems(res.data.requests || []);
    } catch (err) {
      console.error('Failed to load registration requests:', err);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { load(); }, [load]);

  const changeStatus = async (id: string, status: string) => {
    try {
      await updateRegistrationRequest(id, { status });
      load();
    } catch (err) { console.error(err); }
  };

  const saveNotes = async (id: string, admin_notes: string) => {
    try {
      await updateRegistrationRequest(id, { admin_notes });
      load();
    } catch (err) { console.error(err); }
  };

  const remove = async (id: string) => {
    if (!confirm('Supprimer cette demande ?')) return;
    try {
      await deleteRegistrationRequest(id);
      load();
    } catch (err) { console.error(err); }
  };

  const waLink = (r: RegistrationRequest) => {
    const digits = (r.phone || '').replace(/\D/g, '');
    const msg = `Salam ${r.prenom} ! Merci pour ta demande sur Mou3allim. Je te contacte pour activer ton compte.`;
    return `https://wa.me/${digits}?text=${encodeURIComponent(msg)}`;
  };

  const statusStyle: Record<string, string> = {
    pending:   'bg-amber-100 text-amber-800 border-amber-200',
    contacted: 'bg-blue-100 text-blue-800 border-blue-200',
    activated: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    rejected:  'bg-gray-200 text-gray-600 border-gray-300',
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        <h3 className="font-bold text-gray-900 flex items-center gap-2">
          <Inbox className="w-5 h-5 text-indigo-600" /> Demandes d'inscription
          <span className="text-sm text-gray-400 font-normal">({items.length})</span>
        </h3>
        <div className="flex-1" />
        {['', 'pending', 'contacted', 'activated', 'rejected'].map(s => (
          <button key={s || 'all'} onClick={() => setFilter(s)}
            className={`px-3 py-1.5 text-xs rounded-lg font-medium transition ${
              filter === s ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'
            }`}>
            {s === '' ? 'Tous' : s === 'pending' ? 'En attente' : s === 'contacted' ? 'Contactés' : s === 'activated' ? 'Activés' : 'Rejetés'}
          </button>
        ))}
        <button onClick={load}
          className="flex items-center gap-1 px-3 py-1.5 text-sm bg-white border border-gray-200 hover:bg-gray-50 rounded-lg">
          <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} /> Actualiser
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border overflow-hidden">
        {items.length === 0 ? (
          <div className="text-center py-16 text-gray-400">
            <Inbox className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            Aucune demande pour le moment.
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {items.map(r => {
              const alreadyActivated = !!r.created_user_id;
              return (
              <div key={r.id} className="p-5 hover:bg-gray-50 transition">
                <div className="flex items-start gap-4 flex-wrap">
                  <div className="w-11 h-11 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold shadow">
                    {(r.prenom?.[0] || '?').toUpperCase()}{(r.nom?.[0] || '').toUpperCase()}
                  </div>
                  <div className="flex-1 min-w-[220px]">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="font-bold text-gray-900">{r.prenom} {r.nom}</h4>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${statusStyle[r.status] || statusStyle.pending}`}>
                        {r.status}
                      </span>
                      {r.promo_code && <span className="text-xs font-semibold text-indigo-600">· Code {r.promo_code}</span>}
                      {alreadyActivated && (
                        <span className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200">
                          <Check className="w-3 h-3" /> Compte créé
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1 flex-wrap">
                      <span className="flex items-center gap-1"><Phone className="w-3.5 h-3.5" /> {r.phone}</span>
                      <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> {r.ville}</span>
                      {r.email && <span className="flex items-center gap-1"><Mail className="w-3.5 h-3.5" /> {r.email}</span>}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      Reçu le {new Date(r.created_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    {/* ★ Create account button */}
                    {!alreadyActivated && (
                      <button
                        onClick={() => setActivateTarget(r)}
                        className="inline-flex items-center gap-1.5 px-3 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-sm font-semibold rounded-lg shadow-sm transition"
                      >
                        <UserPlus className="w-4 h-4" /> Créer le compte
                      </button>
                    )}
                    <a href={waLink(r)} target="_blank" rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 px-3 py-2 bg-[#25D366] hover:bg-[#1fbb57] text-white text-sm font-semibold rounded-lg shadow-sm transition">
                      <MessageCircle className="w-4 h-4" /> WhatsApp
                    </a>
                    <select value={r.status} onChange={e => changeStatus(r.id, e.target.value)}
                      className="px-2 py-1.5 text-sm border border-gray-200 rounded-lg bg-white">
                      <option value="pending">En attente</option>
                      <option value="contacted">Contacté</option>
                      <option value="activated">Activé</option>
                      <option value="rejected">Rejeté</option>
                    </select>
                    <button onClick={() => setExpandedId(expandedId === r.id ? null : r.id)}
                      className="p-2 text-gray-400 hover:text-gray-700">
                      {expandedId === r.id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                    <button onClick={() => remove(r.id)} className="p-2 text-gray-400 hover:text-red-600">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                {expandedId === r.id && (
                  <div className="mt-4 pl-15 grid md:grid-cols-2 gap-4">
                    {r.message && (
                      <div>
                        <div className="text-xs font-semibold text-gray-500 uppercase mb-1">Message</div>
                        <div className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3 border border-gray-100">{r.message}</div>
                      </div>
                    )}
                    <div>
                      <div className="text-xs font-semibold text-gray-500 uppercase mb-1">Notes admin</div>
                      <AdminNotesEditor initial={r.admin_notes || ''} onSave={v => saveNotes(r.id, v)} />
                    </div>
                  </div>
                )}
              </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ★ Activate Modal */}
      {activateTarget && (
        <ActivateAccountModal
          request={activateTarget}
          onClose={() => setActivateTarget(null)}
          onDone={() => { setActivateTarget(null); load(); }}
        />
      )}
    </div>
  );
}

// ─── Activate Account Modal ──────────────────────────────────

function ActivateAccountModal({
  request: r,
  onClose,
  onDone,
}: {
  request: RegistrationRequest;
  onClose: () => void;
  onDone: () => void;
}) {
  const defaultUsername = `${(r.prenom || '').toLowerCase().replace(/\s/g, '')}.${(r.nom || '').toLowerCase().replace(/\s/g, '')}`;
  const [username, setUsername] = useState(defaultUsername);
  const promoCode = (r.promo_code || '').trim();
  const [password, setPassword] = useState('');
  const [accountType, setAccountType] = useState<'permanent' | 'test'>('permanent');
  const [showPwd, setShowPwd] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState<{ email: string; username: string; expires_at: string | null } | null>(null);

  const handleSubmit = async () => {
    if (!password || password.length < 4) { setError('Mot de passe trop court (min 4 car.)'); return; }
    setSubmitting(true);
    setError('');
    try {
      const res = await activateRegistration(r.id, {
        password,
        account_type: accountType,
        username: username.trim() || undefined,
        promo_code: promoCode.trim() || undefined,
      });
      setSuccess({
        email: res.data.email,
        username: res.data.username,
        expires_at: res.data.expires_at,
      });
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Erreur inconnue';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6" onClick={e => e.stopPropagation()}>
        {success ? (
          /* ── Success screen ── */
          <div className="text-center space-y-4">
            <div className="w-16 h-16 mx-auto rounded-full bg-emerald-100 flex items-center justify-center">
              <Check className="w-8 h-8 text-emerald-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900">Compte créé avec succès !</h3>
            <div className="bg-gray-50 rounded-xl p-4 text-left text-sm space-y-2 border">
              <div className="flex justify-between">
                <span className="text-gray-500">Nom</span>
                <span className="font-semibold">{r.prenom} {r.nom}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Email / identifiant</span>
                <span className="font-mono text-xs">{success.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Nom d'utilisateur</span>
                <span className="font-semibold">{success.username}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Code promo</span>
                <span className="font-semibold">{promoCode || '-'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Mot de passe</span>
                <span className="font-mono">{password}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Type</span>
                <span className={`font-semibold ${accountType === 'test' ? 'text-amber-600' : 'text-emerald-600'}`}>
                  {accountType === 'test' ? '⏱ Test (24h)' : '✅ Permanent'}
                </span>
              </div>
              {success.expires_at && (
                <div className="flex justify-between">
                  <span className="text-gray-500">Expire le</span>
                  <span className="text-amber-600 font-semibold text-xs">
                    {new Date(success.expires_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })}
                  </span>
                </div>
              )}
            </div>
            <p className="text-xs text-gray-500">
              Envoyez ces identifiants à l'élève via WhatsApp.
            </p>
            <button onClick={onDone}
              className="w-full py-2.5 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition">
              Fermer
            </button>
          </div>
        ) : (
          /* ── Form ── */
          <div className="space-y-5">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <UserPlus className="w-5 h-5 text-indigo-600" />
                Créer le compte
              </h3>
              <button onClick={onClose} className="p-1.5 hover:bg-gray-100 rounded-lg">
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            {/* Student info summary */}
            <div className="flex items-center gap-3 bg-gray-50 rounded-xl p-3 border">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-sm">
                {(r.prenom?.[0] || '').toUpperCase()}{(r.nom?.[0] || '').toUpperCase()}
              </div>
              <div>
                <p className="font-bold text-gray-900 text-sm">{r.prenom} {r.nom}</p>
                <p className="text-xs text-gray-500">{r.phone} · {r.ville}</p>
              </div>
            </div>

            {/* Username */}
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1.5">Nom d'utilisateur</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  className="w-full pl-9 pr-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none"
                  placeholder="prenom.nom"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1.5">Code promo (auto)</label>
              <div className="relative">
                <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  value={promoCode || '— aucun —'}
                  readOnly
                  disabled
                  className="w-full pl-9 pr-3 py-2.5 border border-gray-200 rounded-xl text-sm bg-gray-50 text-gray-700 outline-none uppercase cursor-not-allowed"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1.5">Mot de passe</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type={showPwd ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full pl-9 pr-10 py-2.5 border border-gray-200 rounded-xl text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none"
                  placeholder="Choisir un mot de passe"
                />
                <button onClick={() => setShowPwd(!showPwd)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  {showPwd ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Account type */}
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-2">Type de compte</label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setAccountType('permanent')}
                  className={`flex flex-col items-center gap-1.5 p-3 rounded-xl border-2 transition-all ${
                    accountType === 'permanent'
                      ? 'border-emerald-500 bg-emerald-50 shadow-sm'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Check className={`w-5 h-5 ${accountType === 'permanent' ? 'text-emerald-600' : 'text-gray-400'}`} />
                  <span className={`text-sm font-bold ${accountType === 'permanent' ? 'text-emerald-700' : 'text-gray-600'}`}>Permanent</span>
                  <span className="text-[10px] text-gray-500">Accès illimité</span>
                </button>
                <button
                  onClick={() => setAccountType('test')}
                  className={`flex flex-col items-center gap-1.5 p-3 rounded-xl border-2 transition-all ${
                    accountType === 'test'
                      ? 'border-amber-500 bg-amber-50 shadow-sm'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Clock className={`w-5 h-5 ${accountType === 'test' ? 'text-amber-600' : 'text-gray-400'}`} />
                  <span className={`text-sm font-bold ${accountType === 'test' ? 'text-amber-700' : 'text-gray-600'}`}>Test (24h)</span>
                  <span className="text-[10px] text-gray-500">Expire dans 1 jour</span>
                </button>
              </div>
            </div>

            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {error}
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={submitting || !password}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-sm hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2"
            >
              {submitting ? (
                <><RefreshCw className="w-4 h-4 animate-spin" /> Création en cours…</>
              ) : (
                <><UserPlus className="w-4 h-4" /> Créer le compte</>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function AdminNotesEditor({ initial, onSave }: { initial: string; onSave: (v: string) => void }) {
  const [val, setVal] = useState(initial);
  const dirty = val !== initial;
  return (
    <div className="flex gap-2 items-start">
      <textarea value={val} onChange={e => setVal(e.target.value)} rows={2}
        placeholder="Ajoute une note (privée)…"
        className="flex-1 px-3 py-2 text-sm border border-gray-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-none resize-none" />
      {dirty && (
        <button onClick={() => onSave(val)}
          className="px-3 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700">
          Enregistrer
        </button>
      )}
    </div>
  );
}
