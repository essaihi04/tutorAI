import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap, Calculator, Calendar, MapPin, ExternalLink,
  Trophy, Sparkles, ArrowRight, Info, Building2, Clock, Users,
  CheckCircle2, AlertCircle, ChevronDown, ChevronUp,
} from 'lucide-react';
import { getConcoursCatalog, simulateConcours } from '../services/api';

interface School {
  name: string;
  city: string;
  threshold_min: number;
  threshold_strong: number;
}
interface Subject { name: string; duration_min: number; weight: number; }
interface Concours {
  id: string;
  name: string;
  full_name: string;
  type: string;
  level: string;
  duration_years: number;
  tagline: string;
  schools: School[];
  eligible_bacs: string[];
  preselection: { criterion: string; explanation: string };
  exam: { format: string; subjects: Subject[]; total_duration_min: number; month: string } | null;
  oral: { type: string; duration_min: number; weight_pct: number } | null;
  registration: { site: string; period: string; fee_dh: number };
  places_total: number;
  tips: string[];
}
interface Catalog { year: number; concours: Concours[]; note?: string; last_updated?: string; }

interface SimulateResult {
  note_admission: number;
  moyenne_bac_projetee?: number | null;
  formula_explanation: string;
  results: {
    concours_id: string;
    concours_name: string;
    school_name: string;
    city: string;
    threshold_min: number;
    threshold_strong: number;
    chance: { level: string; label: string; color: string; score: number };
  }[];
  summary: { total_schools: number; by_chance: Record<string, number>; top_3: any[] };
}

const TYPE_LABELS: Record<string, { label: string; color: string }> = {
  ingenieur_post_bac: { label: 'Ingénieur', color: 'from-blue-500 to-indigo-600' },
  commerce_post_bac: { label: 'Commerce', color: 'from-emerald-500 to-teal-600' },
  medecine: { label: 'Médecine', color: 'from-rose-500 to-red-600' },
  architecture: { label: 'Architecture', color: 'from-amber-500 to-orange-600' },
  voie_acces_grande_ecole: { label: 'CPGE', color: 'from-purple-500 to-fuchsia-600' },
};

const CHANCE_BADGE: Record<string, string> = {
  forte: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  moyenne: 'bg-amber-50 text-amber-700 border-amber-200',
  faible: 'bg-orange-50 text-orange-700 border-orange-200',
  tres_faible: 'bg-red-50 text-red-700 border-red-200',
};

function ConcoursCard({ c }: { c: Concours }) {
  const [expanded, setExpanded] = useState(false);
  const t = TYPE_LABELS[c.type] || { label: c.type, color: 'from-gray-500 to-gray-700' };

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition overflow-hidden">
      <div className={`bg-gradient-to-r ${t.color} px-5 py-4 text-white`}>
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-[10px] uppercase tracking-widest opacity-80 mb-1">{t.label} · {c.duration_years} ans</div>
            <h3 className="text-xl font-bold leading-tight">{c.name}</h3>
            <p className="text-sm opacity-90 mt-1">{c.tagline}</p>
          </div>
          <div className="text-right shrink-0">
            <div className="text-[10px] uppercase opacity-80">Places</div>
            <div className="text-2xl font-bold">{c.places_total}</div>
          </div>
        </div>
      </div>

      <div className="p-5 space-y-4">
        {/* Quick info */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="flex items-start gap-2">
            <Building2 className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
            <div><div className="text-xs text-gray-500">Écoles</div><div className="font-semibold">{c.schools.length}</div></div>
          </div>
          {c.exam && (
            <div className="flex items-start gap-2">
              <Calendar className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
              <div><div className="text-xs text-gray-500">Concours</div><div className="font-semibold">{c.exam.month}</div></div>
            </div>
          )}
          {c.exam && (
            <div className="flex items-start gap-2">
              <Clock className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
              <div><div className="text-xs text-gray-500">Durée écrit</div><div className="font-semibold">{Math.round(c.exam.total_duration_min / 60)}h</div></div>
            </div>
          )}
          <div className="flex items-start gap-2">
            <Users className="w-4 h-4 text-gray-400 mt-0.5 shrink-0" />
            <div><div className="text-xs text-gray-500">Frais</div><div className="font-semibold">{c.registration.fee_dh > 0 ? `${c.registration.fee_dh} DH` : 'Gratuit'}</div></div>
          </div>
        </div>

        {/* Preselection */}
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-3 text-sm">
          <div className="flex items-center gap-2 text-blue-800 font-semibold mb-1">
            <Trophy className="w-4 h-4" /> Présélection
          </div>
          <div className="text-blue-900/80">{c.preselection.explanation}</div>
        </div>

        {/* Toggle details */}
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full flex items-center justify-between text-sm font-medium text-indigo-700 hover:text-indigo-900 transition"
        >
          <span>{expanded ? 'Masquer' : 'Voir'} le détail (épreuves, écoles, conseils)</span>
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {expanded && (
          <div className="space-y-4 pt-2 border-t border-gray-100">
            {/* Exam */}
            {c.exam && (
              <div>
                <div className="font-semibold text-sm mb-2 text-gray-900">📝 Épreuves écrites — {c.exam.format}</div>
                <ul className="space-y-1">
                  {c.exam.subjects.map((s, i) => (
                    <li key={i} className="flex items-center justify-between text-sm bg-gray-50 px-3 py-1.5 rounded-lg">
                      <span>{s.name}</span>
                      <span className="text-xs text-gray-500">{s.duration_min} min · coef. {s.weight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Oral */}
            {c.oral && (
              <div>
                <div className="font-semibold text-sm mb-2 text-gray-900">🎤 Oral</div>
                <div className="text-sm bg-purple-50 border border-purple-100 rounded-lg px-3 py-2">
                  <div>{c.oral.type}</div>
                  <div className="text-xs text-purple-700 mt-1">Durée ~{c.oral.duration_min} min · {c.oral.weight_pct}% de la note</div>
                </div>
              </div>
            )}

            {/* Schools */}
            <div>
              <div className="font-semibold text-sm mb-2 text-gray-900">🏛 Écoles & seuils estimés (Bac /20)</div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                {c.schools.map((s, i) => (
                  <div key={i} className="flex items-center justify-between text-sm bg-gray-50 px-3 py-1.5 rounded-lg">
                    <span className="flex items-center gap-1.5"><MapPin className="w-3 h-3 text-gray-400" /> {s.name}</span>
                    <span className="text-xs font-medium text-gray-600">{s.threshold_min}–{s.threshold_strong}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Eligible bacs */}
            <div>
              <div className="font-semibold text-sm mb-2 text-gray-900">✅ Bacs éligibles</div>
              <div className="flex flex-wrap gap-1.5">
                {c.eligible_bacs.map((b, i) => (
                  <span key={i} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded-full">{b}</span>
                ))}
              </div>
            </div>

            {/* Tips */}
            {c.tips && c.tips.length > 0 && (
              <div>
                <div className="font-semibold text-sm mb-2 text-gray-900">💡 Conseils</div>
                <ul className="space-y-1">
                  {c.tips.map((t, i) => (
                    <li key={i} className="text-sm text-gray-700 flex gap-2">
                      <Sparkles className="w-3.5 h-3.5 text-amber-500 mt-0.5 shrink-0" />
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Registration footer */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-100 text-sm">
          <div className="text-xs text-gray-500">
            <Calendar className="w-3 h-3 inline mr-1" /> Inscriptions : {c.registration.period}
          </div>
          <a href={c.registration.site} target="_blank" rel="noreferrer"
            className="inline-flex items-center gap-1 text-indigo-700 hover:text-indigo-900 font-medium">
            S'inscrire <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}

function ChanceCalculator() {
  const [regional, setRegional] = useState('');
  const [national, setNational] = useState('');
  const [showCpgeFields, setShowCpgeFields] = useState(false);
  const [cc1, setCc1] = useState('');
  const [cc2, setCc2] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SimulateResult | null>(null);
  const [error, setError] = useState('');

  const submit = async () => {
    setError(''); setResult(null); setLoading(true);
    try {
      const payload: any = {
        regional: parseFloat(regional),
        national_estimated: parseFloat(national),
      };
      if (showCpgeFields) {
        if (cc1) payload.cc1 = parseFloat(cc1);
        if (cc2) payload.cc2 = parseFloat(cc2);
      }
      const { data } = await simulateConcours(payload);
      setResult(data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Erreur. Vérifie tes notes (entre 0 et 20).');
    } finally { setLoading(false); }
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 via-white to-purple-50 rounded-3xl border border-indigo-200 shadow-lg p-6 md:p-8">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-md">
          <Calculator className="w-6 h-6 text-white" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Calculateur de chances</h2>
          <p className="text-sm text-gray-600">Calcule ta note de présélection et découvre tes concours accessibles.</p>
        </div>
      </div>

      {/* Formula explanation */}
      <div className="mt-4 mb-5 p-4 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl">
        <div className="flex items-start gap-2">
          <Info className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="text-sm">
            <div className="font-bold text-amber-900 mb-1">Formule officielle 2025-2026</div>
            <div className="text-amber-900/90">
              <b>Note d'admission concours = 0,75 × Examen National + 0,25 × Examen Régional</b><br />
              <span className="text-xs italic">⚠️ Le contrôle continu n'est <b>PAS</b> pris en compte pour les concours communs (ENSA, ENSAM, ENCG, FMP, ENA).</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Examen Régional <span className="text-red-500">*</span>
              <span className="text-gray-400 text-xs ml-1">(1ère bac, déjà passé)</span>
            </label>
            <input type="number" min={0} max={20} step={0.01} value={regional} onChange={e => setRegional(e.target.value)}
              placeholder="Ex : 14.50"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-lg font-semibold" />
            <div className="text-[11px] text-gray-500 mt-1">Compte pour 25 % de ta note de présélection</div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Note projetée Examen National <span className="text-red-500">*</span>
            </label>
            <input type="number" min={0} max={20} step={0.01} value={national} onChange={e => setNational(e.target.value)}
              placeholder="Ex : 13.00"
              className="w-full px-4 py-3 border border-indigo-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-lg font-semibold bg-indigo-50/30" />
            <div className="text-[11px] text-indigo-700 font-medium mt-1">⭐ Compte pour 75 % — c'est le plus important !</div>
          </div>
        </div>

        {/* Optional CPGE fields */}
        <button
          type="button"
          onClick={() => setShowCpgeFields(!showCpgeFields)}
          className="mt-4 text-xs text-purple-700 hover:text-purple-900 font-medium underline"
        >
          {showCpgeFields ? '− Masquer' : '+ Ajouter mes notes de Contrôle Continu'} (utile pour CPGE / moyenne du Bac)
        </button>

        {showCpgeFields && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3 p-3 bg-purple-50 rounded-lg">
            <div>
              <label className="block text-xs font-medium text-purple-900 mb-1">CC 1ère bac</label>
              <input type="number" min={0} max={20} step={0.01} value={cc1} onChange={e => setCc1(e.target.value)}
                placeholder="Ex : 15.20" className="w-full px-3 py-2 border border-purple-200 rounded-lg text-sm" />
            </div>
            <div>
              <label className="block text-xs font-medium text-purple-900 mb-1">CC 2ème bac (en cours)</label>
              <input type="number" min={0} max={20} step={0.01} value={cc2} onChange={e => setCc2(e.target.value)}
                placeholder="Ex : 14.80" className="w-full px-3 py-2 border border-purple-200 rounded-lg text-sm" />
            </div>
            <div className="col-span-full text-[11px] text-purple-700">
              💡 Le CC sert uniquement à calculer ta moyenne officielle du Bac (25% CC + 25% Régional + 50% National). Il n'influence pas la note de présélection des concours.
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-3 flex items-center gap-2 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          <AlertCircle className="w-4 h-4" /> {error}
        </div>
      )}

      <button onClick={submit} disabled={loading}
        className="w-full mt-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-md hover:shadow-lg transition disabled:opacity-50 flex items-center justify-center gap-2">
        {loading ? 'Calcul…' : <>Découvrir mes concours <ArrowRight className="w-4 h-4" /></>}
      </button>

      {result && (
        <div className="mt-6 space-y-4">
          {/* Score banner */}
          <div className="bg-white rounded-2xl border border-indigo-200 p-5">
            <div className="text-xs uppercase tracking-wider text-indigo-600 font-bold mb-1">Note d'admission concours (75% N + 25% R)</div>
            <div className="flex items-end gap-2">
              <div className="text-5xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                {result.note_admission.toFixed(2)}
              </div>
              <div className="text-2xl text-gray-400 mb-1">/20</div>
            </div>
            {result.moyenne_bac_projetee != null && (
              <div className="text-xs text-gray-500 mt-2 border-t border-gray-100 pt-2">
                <b>Moyenne officielle du Bac (avec CC) :</b> <span className="font-semibold text-gray-800">{result.moyenne_bac_projetee.toFixed(2)}/20</span>
                <span className="text-[10px] text-gray-400 ml-2">— affichée sur ton diplôme, mais pas utilisée pour les concours.</span>
              </div>
            )}
            <div className="grid grid-cols-4 gap-2 mt-4 text-center">
              <div className="bg-emerald-50 rounded-lg p-2"><div className="text-2xl font-bold text-emerald-700">{result.summary.by_chance.forte || 0}</div><div className="text-xs text-emerald-600">forte</div></div>
              <div className="bg-amber-50 rounded-lg p-2"><div className="text-2xl font-bold text-amber-700">{result.summary.by_chance.moyenne || 0}</div><div className="text-xs text-amber-600">moyenne</div></div>
              <div className="bg-orange-50 rounded-lg p-2"><div className="text-2xl font-bold text-orange-700">{result.summary.by_chance.faible || 0}</div><div className="text-xs text-orange-600">faible</div></div>
              <div className="bg-red-50 rounded-lg p-2"><div className="text-2xl font-bold text-red-700">{result.summary.by_chance.tres_faible || 0}</div><div className="text-xs text-red-600">peu probable</div></div>
            </div>
          </div>

          {/* Detailed list */}
          <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div className="px-5 py-3 bg-gray-50 border-b font-semibold text-sm">Résultats détaillés ({result.results.length} écoles)</div>
            <div className="divide-y divide-gray-100 max-h-96 overflow-y-auto">
              {result.results.map((r, i) => (
                <div key={i} className="px-5 py-3 flex items-center justify-between gap-3 hover:bg-gray-50 transition">
                  <div className="min-w-0">
                    <div className="font-medium text-sm truncate">{r.school_name}</div>
                    <div className="text-xs text-gray-500">{r.concours_name} · seuil {r.threshold_min}–{r.threshold_strong}</div>
                  </div>
                  <span className={`text-xs px-2.5 py-1 rounded-full border font-medium whitespace-nowrap ${CHANCE_BADGE[r.chance.level]}`}>
                    {r.chance.label}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="text-center pt-2">
            <Link to="/signup" className="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-black text-white rounded-xl font-semibold transition">
              <Sparkles className="w-4 h-4" /> Crée un compte gratuit pour suivre ces concours
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default function Orientation() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [filter, setFilter] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getConcoursCatalog().then(r => setCatalog(r.data)).finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    if (!catalog) return [];
    if (filter === 'all') return catalog.concours;
    return catalog.concours.filter(c => c.type === filter);
  }, [catalog, filter]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero */}
      <div className="bg-gradient-to-br from-indigo-900 via-purple-900 to-fuchsia-900 text-white">
        <div className="max-w-6xl mx-auto px-4 py-12 md:py-16">
          <Link to="/" className="text-sm text-indigo-200 hover:text-white inline-flex items-center gap-1 mb-4">
            ← Retour à l'accueil
          </Link>
          <div className="flex items-center gap-3 mb-3">
            <GraduationCap className="w-8 h-8" />
            <span className="text-sm uppercase tracking-widest text-indigo-200">Orientation Post-BAC</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold leading-tight">
            Le BAC, c'est le début.<br />
            <span className="bg-gradient-to-r from-amber-300 to-pink-300 bg-clip-text text-transparent">
              Prépare aussi tes concours.
            </span>
          </h1>
          <p className="mt-4 text-lg text-indigo-100 max-w-2xl">
            Découvre les <b>concours communs post-BAC</b> au Maroc — un seul concours, plusieurs écoles. Calcule tes chances en temps réel et choisis ta voie.
          </p>
        </div>
      </div>

      {/* Calculator */}
      <div className="max-w-6xl mx-auto px-4 -mt-8 relative z-10">
        <ChanceCalculator />
      </div>

      {/* Catalog */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900">Concours communs post-BAC</h2>
            <p className="text-sm text-gray-600 mt-1">
              Ces concours regroupent <b>plusieurs écoles avec une seule épreuve</b>. Tu maximises tes chances en t'inscrivant une seule fois.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            {[
              { key: 'all', label: 'Tous' },
              { key: 'ingenieur_post_bac', label: 'Ingénieur' },
              { key: 'medecine', label: 'Médecine' },
              { key: 'commerce_post_bac', label: 'Commerce' },
              { key: 'architecture', label: 'Architecture' },
              { key: 'voie_acces_grande_ecole', label: 'CPGE' },
            ].map(f => (
              <button key={f.key} onClick={() => setFilter(f.key)}
                className={`px-3 py-1.5 text-sm font-medium rounded-lg transition ${
                  filter === f.key ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}>{f.label}</button>
            ))}
          </div>
        </div>

        {loading && (
          <div className="text-center py-16 text-gray-500">Chargement…</div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="text-center py-16 text-gray-500">Aucun concours dans cette catégorie.</div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {filtered.map(c => <ConcoursCard key={c.id} c={c} />)}
        </div>

        {catalog?.note && (
          <div className="mt-8 text-xs text-gray-500 italic flex items-start gap-2 max-w-3xl">
            <Info className="w-4 h-4 shrink-0 mt-0.5" />
            <div><b>Note :</b> {catalog.note}{catalog.last_updated && ` (Dernière mise à jour : ${catalog.last_updated})`}</div>
          </div>
        )}
      </div>

      {/* CTA bottom */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <CheckCircle2 className="w-12 h-12 mx-auto mb-3 opacity-80" />
          <h3 className="text-2xl md:text-3xl font-bold mb-2">Prépare ton BAC ET tes concours sur la même plateforme</h3>
          <p className="text-indigo-100 mb-6 max-w-2xl mx-auto">
            moalim.online est la seule plateforme marocaine qui te suit du lycée à ta grande école — annales corrigées par IA, examens blancs et coach d'orientation.
          </p>
          <Link to="/signup" className="inline-flex items-center gap-2 px-7 py-3.5 bg-white text-indigo-700 rounded-xl font-bold hover:bg-gray-100 transition">
            Créer mon compte gratuit <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
