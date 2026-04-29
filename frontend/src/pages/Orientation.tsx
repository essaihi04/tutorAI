import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap, Calculator, Calendar, ArrowRight, ExternalLink, AlertCircle,
  Briefcase, TrendingUp, Sparkles, Plane, Compass,
} from 'lucide-react';
import { getConcoursCatalog, simulateConcours, type SimulateInput } from '../services/api';

type Catalog = any;

type SimulateResult = {
  note_admission: number;
  moyenne_bac_projetee?: number | null;
  bac_type: string;
  components: Record<string, any>;
  results: Array<{
    concours_id: string;
    concours_name: string;
    type: string;
    tagline?: string;
    seuil: number | null;
    status: { level: string; label: string; color: string; margin: number | null; score: number };
    schools_count: number;
    registration_site?: string;
    places_total?: number;
  }>;
  summary: { total_concours: number; preselected_count: number; by_level: Record<string, number> };
  formula_explanation: string;
};

const BAC_OPTIONS = [
  { key: 'sm', label: 'Sciences Mathématiques (A/B)' },
  { key: 'se_pc', label: 'Sciences Expérimentales — PC' },
  { key: 'se_svt', label: 'Sciences Expérimentales — SVT' },
  { key: 'se_agro', label: 'Sciences Expérimentales — Agronomiques' },
  { key: 'tech', label: 'Sciences et Technologies' },
  { key: 'pro', label: 'Baccalauréat Professionnel' },
  { key: 'eco', label: 'Sciences Économiques / Gestion' },
  { key: 'lettres', label: 'Lettres et Sciences Humaines' },
];

// ─── Profile quiz ───────────────────────────────────────────────
type QuizQ = { id: string; q: string; choices: { label: string; tags: string[] }[] };

const QUIZ: QuizQ[] = [
  {
    id: 'matieres',
    q: 'Quelles matières te passionnent le plus ?',
    choices: [
      { label: 'Maths et physique', tags: ['maths', 'physique', 'sciences'] },
      { label: 'SVT, biologie, santé', tags: ['biologie', 'sante', 'sciences'] },
      { label: 'Économie, gestion, chiffres', tags: ['chiffres', 'commerce', 'gestion'] },
      { label: 'Arts, dessin, créativité', tags: ['art', 'dessin', 'creatif', 'visuel'] },
      { label: 'Langues, philo, sciences humaines', tags: ['communication', 'culture', 'social'] },
    ],
  },
  {
    id: 'travail',
    q: 'Quel type de travail te ressemble le plus ?',
    choices: [
      { label: 'Résoudre des problèmes techniques', tags: ['resolution_problemes', 'tech', 'maths'] },
      { label: 'Aider et soigner les gens', tags: ['empathie', 'sante', 'social'] },
      { label: 'Vendre, négocier, manager', tags: ['communication', 'commerce', 'social'] },
      { label: 'Créer, concevoir, dessiner', tags: ['creatif', 'art', 'manuel'] },
      { label: 'Construire, fabriquer, expérimenter', tags: ['mecanique', 'manuel', 'industrie'] },
    ],
  },
  {
    id: 'rythme',
    q: "Quel rythme d'études acceptes-tu ?",
    choices: [
      { label: 'Très intense, 35h+/semaine (CPGE)', tags: ['intense', 'competitif', 'resistant_stress'] },
      { label: "Soutenu mais structuré (école d'ingénieur)", tags: ['tech', 'travail_equipe'] },
      { label: 'Équilibré, pratique sur le terrain', tags: ['polyvalent', 'manuel'] },
      { label: 'Long mais valorisant (médecine 7+ ans)', tags: ['long_terme', 'sante', 'resistant_stress'] },
    ],
  },
  {
    id: 'avenir',
    q: "Qu'est-ce qui compte le plus pour ton avenir ?",
    choices: [
      { label: "Sécurité de l'emploi et bon salaire", tags: ['tech', 'sante', 'gestion'] },
      { label: 'Prestige du diplôme et carrière internationale', tags: ['prestige', 'international'] },
      { label: 'Liberté de créer / entreprendre', tags: ['creatif', 'entrepreneuriat'] },
      { label: 'Aider la société / utilité publique', tags: ['social', 'sante', 'empathie'] },
    ],
  },
  {
    id: 'mobilite',
    q: "Es-tu prêt(e) à partir travailler à l'étranger ?",
    choices: [
      { label: "Oui, c'est même un objectif", tags: ['international'] },
      { label: 'Pourquoi pas, si bonne opportunité', tags: ['international'] },
      { label: 'Non, je veux rester au Maroc', tags: [] },
    ],
  },
];

function badgeMarche(level?: string): string {
  if (level === 'très_forte') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  if (level === 'forte') return 'bg-green-50 text-green-700 border-green-200';
  if (level === 'moyenne') return 'bg-amber-50 text-amber-700 border-amber-200';
  return 'bg-gray-50 text-gray-600 border-gray-200';
}

function badgeClass(level: string): string {
  switch (level) {
    case 'admis_large':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200';
    case 'admis':
      return 'bg-green-50 text-green-700 border border-green-200';
    case 'limite':
      return 'bg-amber-50 text-amber-700 border border-amber-200';
    case 'proche':
      return 'bg-orange-50 text-orange-700 border border-orange-200';
    case 'echec':
      return 'bg-red-50 text-red-700 border border-red-200';
    default:
      return 'bg-gray-50 text-gray-700 border border-gray-200';
  }
}

export default function Orientation() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [loadingCatalog, setLoadingCatalog] = useState(true);

  const [bacType, setBacType] = useState<string>('se_pc');
  const [regional, setRegional] = useState<string>('');
  const [national, setNational] = useState<string>('');
  const [cc1, setCc1] = useState<string>('');
  const [cc2, setCc2] = useState<string>('');
  const [showCpge, setShowCpge] = useState<boolean>(false);

  const [simLoading, setSimLoading] = useState(false);
  const [simError, setSimError] = useState<string>('');
  const [sim, setSim] = useState<SimulateResult | null>(null);

  // Quiz state: answers[questionId] = chosenIndex
  const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({});
  const [showQuiz, setShowQuiz] = useState<boolean>(false);
  const [quizRevealed, setQuizRevealed] = useState<boolean>(false);

  useEffect(() => {
    getConcoursCatalog()
      .then((res) => setCatalog(res.data))
      .finally(() => setLoadingCatalog(false));
  }, []);

  // ─── Quiz scoring ────────────────────────────────────────────────
  const quizComplete = QUIZ.every((q) => quizAnswers[q.id] !== undefined);

  const userTags: string[] = useMemo(() => {
    const tags: string[] = [];
    for (const q of QUIZ) {
      const idx = quizAnswers[q.id];
      if (idx !== undefined) tags.push(...q.choices[idx].tags);
    }
    return tags;
  }, [quizAnswers]);

  const concoursScored = useMemo(() => {
    if (!catalog?.concours) return [] as Array<{ c: any; score: number }>;
    return (catalog.concours as any[])
      .map((c) => {
        const tags: string[] = c.profile_tags || [];
        const score = userTags.reduce((acc, t) => acc + (tags.includes(t) ? 1 : 0), 0);
        return { c, score };
      })
      .sort((a, b) => b.score - a.score);
  }, [catalog, userTags]);

  const topMatches = quizComplete ? concoursScored.slice(0, 3) : [];
  const answeredCount = Object.keys(quizAnswers).length;

  const submit = async () => {
    setSimError('');
    setSim(null);
    setSimLoading(true);
    try {
      const payload: SimulateInput = {
        bac_type: bacType as any,
        regional: parseFloat(regional),
        national_estimated: parseFloat(national),
        ...(cc1 ? { cc1: parseFloat(cc1) } : {}),
        ...(cc2 ? { cc2: parseFloat(cc2) } : {}),
      };
      const { data } = await simulateConcours(payload);
      setSim(data);
    } catch (e: any) {
      setSimError(e?.response?.data?.detail || 'Erreur de calcul. Vérifie tes notes (0–20).');
    } finally {
      setSimLoading(false);
    }
  };

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
            Prépare tes concours communs
            <span className="bg-gradient-to-r from-amber-300 to-pink-300 bg-clip-text text-transparent"> 2025-2026</span>
          </h1>
          <p className="mt-4 text-lg text-indigo-100 max-w-2xl">
            Formule officielle de présélection : <b>0,75 × National + 0,25 × Régional</b> — le contrôle continu n'est <b>pas</b> pris en compte.
          </p>
        </div>
      </div>

      {/* Calculator */}
      <div className="max-w-6xl mx-auto px-4 -mt-8 relative z-10">
        <div className="bg-white rounded-3xl border border-indigo-200 shadow-lg p-6 md:p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-md">
              <Calculator className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Calculateur de chances</h2>
              <p className="text-sm text-gray-600">Entre ta filière de Bac, ta note du Régional et ta note nationale projetée.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Filière du Baccalauréat</label>
              <select
                value={bacType}
                onChange={(e) => setBacType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              >
                {BAC_OPTIONS.map((o) => (
                  <option key={o.key} value={o.key}>
                    {o.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Examen Régional (1ère bac)</label>
              <input
                type="number"
                min={0}
                max={20}
                step={0.01}
                value={regional}
                onChange={(e) => setRegional(e.target.value)}
                placeholder="Ex : 14.50"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
              <div className="text-[11px] text-gray-500 mt-1">Pondération 25 %</div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Note projetée Examen National</label>
              <input
                type="number"
                min={0}
                max={20}
                step={0.01}
                value={national}
                onChange={(e) => setNational(e.target.value)}
                placeholder="Ex : 13.00"
                className="w-full px-3 py-2 border border-indigo-300 rounded-lg focus:ring-2 focus:ring-indigo-500 bg-indigo-50/30"
              />
              <div className="text-[11px] text-indigo-700 font-medium mt-1">Pondération 75 %</div>
            </div>
          </div>

          <button
            onClick={submit}
            disabled={simLoading}
            className="w-full mt-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-md hover:shadow-lg transition disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {simLoading ? 'Calcul…' : (
              <>
                Découvrir mes concours <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

          <button
            type="button"
            onClick={() => setShowCpge((s) => !s)}
            className="mt-3 text-xs text-purple-700 hover:text-purple-900 font-medium underline"
          >
            {showCpge ? '− Masquer' : '+ Ajouter mes notes de Contrôle Continu'} (utile pour calculer la moyenne officielle du Bac)
          </button>
          {showCpge && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3 p-3 bg-purple-50 rounded-lg">
              <div>
                <label className="block text-xs font-medium text-purple-900 mb-1">CC 1ère bac</label>
                <input
                  type="number"
                  min={0}
                  max={20}
                  step={0.01}
                  value={cc1}
                  onChange={(e) => setCc1(e.target.value)}
                  placeholder="Ex : 15.20"
                  className="w-full px-3 py-2 border border-purple-200 rounded-lg text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-purple-900 mb-1">CC 2ème bac</label>
                <input
                  type="number"
                  min={0}
                  max={20}
                  step={0.01}
                  value={cc2}
                  onChange={(e) => setCc2(e.target.value)}
                  placeholder="Ex : 14.80"
                  className="w-full px-3 py-2 border border-purple-200 rounded-lg text-sm"
                />
              </div>
              <div className="col-span-full text-[11px] text-purple-700">
                Le contrôle continu n'est pas utilisé pour la présélection concours, uniquement pour la moyenne officielle du Bac.
              </div>
            </div>
          )}

          {simError && (
            <div className="mt-3 flex items-center gap-2 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              <AlertCircle className="w-4 h-4" /> {simError}
            </div>
          )}

          {sim && (
            <div className="mt-6 space-y-4">
              <div className="bg-white rounded-2xl border border-indigo-200 p-5">
                <div className="text-xs uppercase tracking-wider text-indigo-600 font-bold mb-1">
                  Note de présélection (75% N + 25% R)
                </div>
                <div className="flex items-end gap-2">
                  <div className="text-5xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                    {sim.note_admission.toFixed(2)}
                  </div>
                  <div className="text-2xl text-gray-400 mb-1">/20</div>
                </div>
                {sim.moyenne_bac_projetee != null && (
                  <div className="text-xs text-gray-500 mt-2 border-t border-gray-100 pt-2">
                    <b>Moyenne officielle du Bac (avec CC) :</b>
                    <span className="font-semibold text-gray-800"> {sim.moyenne_bac_projetee!.toFixed(2)}/20</span>
                    <span className="text-[10px] text-gray-400 ml-2">— affichée sur le diplôme, pas utilisée pour les concours.</span>
                  </div>
                )}
                <div className="grid grid-cols-3 gap-2 mt-4 text-center">
                  <div className="bg-emerald-50 rounded-lg p-2">
                    <div className="text-2xl font-bold text-emerald-700">{sim.summary.by_level['admis_large'] || 0}</div>
                    <div className="text-xs text-emerald-600">largement</div>
                  </div>
                  <div className="bg-amber-50 rounded-lg p-2">
                    <div className="text-2xl font-bold text-amber-700">{(sim.summary.by_level['admis'] || 0) + (sim.summary.by_level['limite'] || 0)}</div>
                    <div className="text-xs text-amber-600">à la limite</div>
                  </div>
                  <div className="bg-red-50 rounded-lg p-2">
                    <div className="text-2xl font-bold text-red-700">{(sim.summary.by_level['proche'] || 0) + (sim.summary.by_level['echec'] || 0)}</div>
                    <div className="text-xs text-red-600">en dessous</div>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
                <div className="px-5 py-3 bg-gray-50 border-b font-semibold text-sm">Résultats détaillés ({sim.results.length} concours)</div>
                <div className="divide-y divide-gray-100">
                  {sim.results.map((r) => (
                    <div key={r.concours_id} className="px-5 py-3 flex items-center justify-between gap-3 hover:bg-gray-50 transition">
                      <div className="min-w-0">
                        <div className="font-medium text-sm truncate">{r.concours_name}</div>
                        <div className="text-xs text-gray-500">Seuil {r.seuil ?? '—'} · {r.tagline || r.type}</div>
                      </div>
                      <span className={`text-xs px-2.5 py-1 rounded-full font-medium whitespace-nowrap ${badgeClass(r.status.level)}`}>
                        {r.status.label}{typeof r.status.margin === 'number' ? ` (${r.status.margin >= 0 ? '+' : ''}${r.status.margin})` : ''}
                      </span>
                      <a
                        className="text-xs text-indigo-700 hover:text-indigo-900 underline whitespace-nowrap"
                        href={r.registration_site || '#'}
                        target="_blank"
                        rel="noreferrer"
                      >
                        S'inscrire <ExternalLink className="inline w-3 h-3" />
                      </a>
                    </div>
                  ))}
                </div>
              </div>

              <div className="text-center pt-2">
                <Link
                  to="/signup"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-black text-white rounded-xl font-semibold transition"
                >
                  Créer un compte gratuit <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quiz d'orientation */}
      <div className="max-w-6xl mx-auto px-4 mt-12">
        <div className="bg-gradient-to-br from-pink-50 via-amber-50 to-orange-50 border border-pink-200 rounded-3xl p-6 md:p-8">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-md">
                <Compass className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Quelle filière est faite pour toi ?</h2>
                <p className="text-sm text-gray-600">5 questions — 1 minute. On te recommande les concours adaptés à ton profil.</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setShowQuiz((s) => !s)}
              className="px-4 py-2 bg-white border border-pink-300 hover:bg-pink-50 rounded-xl text-sm font-medium text-pink-700"
            >
              {showQuiz ? 'Masquer' : 'Commencer'}
            </button>
          </div>

          {showQuiz && (
            <div className="mt-5 space-y-4">
              {QUIZ.map((q) => (
                <div key={q.id} className="bg-white rounded-2xl border border-pink-100 p-4">
                  <div className="font-semibold text-gray-900 mb-2">{q.q}</div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {q.choices.map((ch, i) => {
                      const selected = quizAnswers[q.id] === i;
                      return (
                        <button
                          key={i}
                          onClick={() => setQuizAnswers((a) => ({ ...a, [q.id]: i }))}
                          className={`text-left text-sm px-3 py-2 rounded-lg border transition ${
                            selected
                              ? 'bg-pink-50 border-pink-400 text-pink-900 font-medium'
                              : 'bg-white border-gray-200 hover:border-pink-300'
                          }`}
                        >
                          {ch.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}

              {/* Reveal button */}
              <div className="flex flex-col items-center gap-2 pt-1">
                <button
                  type="button"
                  disabled={!quizComplete}
                  onClick={() => setQuizRevealed(true)}
                  className="px-6 py-3 bg-gradient-to-r from-pink-600 to-orange-500 hover:from-pink-700 hover:to-orange-600 text-white font-semibold rounded-xl shadow-md disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4" /> Voir ma filière idéale
                </button>
                {!quizComplete && (
                  <div className="text-xs text-gray-500">{answeredCount} / {QUIZ.length} questions répondues — termine pour découvrir ta filière.</div>
                )}
              </div>

              {quizRevealed && quizComplete && topMatches.length > 0 && (
                <div className="bg-white rounded-2xl border-2 border-pink-300 p-5 mt-2">
                  <div className="flex items-center gap-2 mb-3">
                    <Sparkles className="w-5 h-5 text-pink-600" />
                    <div className="font-bold text-gray-900">Tes 3 concours les plus compatibles</div>
                  </div>
                  <div className="space-y-2">
                    {topMatches.map(({ c, score }, idx) => (
                      <div key={c.id} className="flex items-center justify-between gap-3 bg-gradient-to-r from-pink-50 to-orange-50 rounded-lg px-3 py-2">
                        <div className="flex items-center gap-3 min-w-0">
                          <div className="w-8 h-8 bg-pink-600 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                            {idx + 1}
                          </div>
                          <div className="min-w-0">
                            <div className="font-semibold text-sm truncate">{c.name}</div>
                            <div className="text-[11px] text-gray-500 truncate">{c.tagline}</div>
                          </div>
                        </div>
                        <div className="text-xs text-pink-700 font-bold whitespace-nowrap">{score} pts d'affinité</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Catalog (seuils par Bac) */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="flex items-end justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-gray-900">Seuils nationaux {catalog?.year || '—'}</h2>
            <p className="text-sm text-gray-600 mt-1">
              Seuils de <b>présélection 2025-2026</b> par filière de Bac. Identiques pour toutes les écoles d'un même concours.
            </p>
          </div>
          <div>
            <select
              value={bacType}
              onChange={(e) => setBacType(e.target.value)}
              className="px-3 py-2 text-sm rounded-lg border border-gray-200"
            >
              {BAC_OPTIONS.map((o) => (
                <option key={o.key} value={o.key}>
                  {o.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {loadingCatalog && <div className="text-center py-12 text-gray-500">Chargement…</div>}

        {!loadingCatalog && catalog && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {(catalog.concours || []).map((c: any) => (
              <div key={c.id} className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition overflow-hidden">
                <div className="px-5 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
                  <div className="text-[10px] uppercase tracking-widest opacity-80 mb-1">{c.type}</div>
                  <div className="text-xl font-bold">{c.name}</div>
                  {c.tagline && <div className="text-sm opacity-90 mt-1">{c.tagline}</div>}
                </div>
                <div className="p-5 space-y-3">
                  <div className="text-sm text-gray-700">
                    <b>Seuil {BAC_OPTIONS.find((b) => b.key === bacType)?.label} :</b>{' '}
                    <span className="font-semibold">{typeof c.seuils_preselection_2025?.[bacType] === 'number' ? c.seuils_preselection_2025[bacType] : '—'}</span>
                  </div>

                  {/* Débouchés */}
                  {c.debouches && (
                    <div className="bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200 rounded-xl p-3 space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800 uppercase tracking-wide">
                          <TrendingUp className="w-3.5 h-3.5" /> Avenir & débouchés
                        </div>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full border ${badgeMarche(c.debouches.demande_marche)} font-medium uppercase tracking-wide`}>
                          Marché {c.debouches.demande_marche?.replace('_', ' ')}
                        </span>
                      </div>
                      <div className="text-xs text-gray-700 leading-relaxed">{c.debouches.avenir}</div>
                      <div className="flex flex-wrap gap-1">
                        {(c.debouches.metiers || []).slice(0, 4).map((m: string, i: number) => (
                          <span key={i} className="inline-flex items-center gap-1 text-[10px] bg-white border border-emerald-200 text-emerald-800 rounded-full px-2 py-0.5">
                            <Briefcase className="w-2.5 h-2.5" /> {m}
                          </span>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-[11px] text-emerald-900 pt-1 border-t border-emerald-200">
                        <div>Salaire début : <b>{c.debouches.salaire_debut_dh?.[0]}–{c.debouches.salaire_debut_dh?.[1]} DH</b></div>
                        <div>Emploi 6m : <b>{c.debouches.taux_emploi_6mois}%</b></div>
                        {c.debouches.emigration_facile && (
                          <span className="inline-flex items-center gap-0.5 text-blue-700"><Plane className="w-3 h-3" /> International</span>
                        )}
                      </div>
                    </div>
                  )}

                  <div className="flex items-center justify-between text-sm gap-2">
                    <div className="text-gray-500">Écoles : <b>{(c.schools || []).length}</b></div>
                    <a
                      href={c.registration?.site || '#'}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-indigo-700 hover:text-indigo-900 font-medium"
                      title={c.registration?.site}
                    >
                      S'inscrire sur {(c.registration?.site || '').replace(/^https?:\/\//, '').replace(/\/$/, '')}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Info: registration platforms */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-2xl p-4 text-sm text-blue-900">
          <div className="font-semibold mb-1 flex items-center gap-2">
            <ExternalLink className="w-4 h-4" /> Où s'inscrire ?
          </div>
          <ul className="list-disc pl-5 space-y-0.5 text-blue-800">
            <li><b>cursussup.gov.ma</b> — plateforme officielle centralisée pour <b>ENSA, ENSAM, ENCG, Médecine, Architecture</b>. Une seule inscription, plusieurs vœux.</li>
            <li><b>cpge.ac.ma</b> — plateforme séparée et gratuite pour les <b>Classes Préparatoires (CPGE)</b>.</li>
            <li>Les <b>académies militaires</b> (Air, Marine), <b>IAV Hassan II</b> (véto/agro) et <b>écoles privées</b> ont leurs propres sites — à consulter directement.</li>
          </ul>
        </div>

        {/* Step-by-step registration guide */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
            <div className="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
              <div className="text-[10px] uppercase tracking-widest opacity-80">Procédure</div>
              <div className="font-bold">Inscription sur cursussup.gov.ma</div>
              <div className="text-xs opacity-90 mt-1">ENSA · ENSAM · ENCG · Médecine · Architecture</div>
            </div>
            <ol className="p-5 space-y-2.5 text-sm text-gray-800 list-decimal list-inside">
              <li>Crée ton compte sur <b>cursussup.gov.ma</b> avec ton <b>CNE</b> (code Massar) et ton <b>CIN</b>.</li>
              <li>Remplis ton dossier : informations personnelles, filière du Bac, notes du régional.</li>
              <li>Téléverse les pièces : photo, CIN, relevé de notes 1<sup>ère</sup> bac, attestation de scolarité.</li>
              <li>Choisis tes <b>concours</b> et classe tes <b>vœux</b> par ordre de préférence (écoles + villes).</li>
              <li>Paye les frais en ligne (≈ 250–300 DH par concours).</li>
              <li>Valide et <b>imprime ton récépissé</b> (à garder précieusement).</li>
              <li>Surveille les <b>listes de présélection</b> mi-juillet sur ton espace cursussup.</li>
              <li>Si présélectionné : présente-toi à la <b>convocation écrite</b> avec CIN + récépissé.</li>
            </ol>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
            <div className="px-5 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white">
              <div className="text-[10px] uppercase tracking-widest opacity-80">Procédure</div>
              <div className="font-bold">Inscription sur cpge.ac.ma</div>
              <div className="text-xs opacity-90 mt-1">Classes Préparatoires — gratuit</div>
            </div>
            <ol className="p-5 space-y-2.5 text-sm text-gray-800 list-decimal list-inside">
              <li>Dès la <b>publication des résultats du Bac</b>, va sur <b>cpge.ac.ma</b>.</li>
              <li>Crée ton compte avec <b>CNE</b> et <b>CIN</b> (inscription gratuite).</li>
              <li>Saisis tes notes du Bac et tes notes de 1<sup>ère</sup> et 2<sup>ème</sup> année.</li>
              <li>Classe <b>6 lycées</b> par ordre de préférence (selon ta filière : MPSI, PCSI, BCPST, ECT…).</li>
              <li>Téléverse <b>relevés de notes</b>, <b>attestations</b> et <b>avis du conseil de classe</b>.</li>
              <li>Utilise le <b>simulateur officiel</b> : cpge.ac.ma/cand/simulation.aspx pour estimer tes chances.</li>
              <li>Affectation officielle fin juillet — début août.</li>
            </ol>
          </div>
        </div>

        {/* Helpful tip */}
        <div className="mt-4 text-xs text-gray-500 bg-amber-50 border border-amber-200 rounded-xl p-3">
          <b className="text-amber-800">Astuce :</b> Inscris-toi sur <b>plusieurs concours</b> pour multiplier tes chances (cursussup + CPGE en parallèle, c'est très courant). Prépare un dossier numérique avec toutes tes pièces scannées à l'avance.
        </div>

      {/* Calendar 2025 */}
        {catalog?.calendar_2025 && (
          <div className="mt-12 bg-white border border-gray-200 rounded-2xl overflow-hidden">
            <div className="px-5 py-4 bg-gray-50 border-b flex items-center gap-2">
              <Calendar className="w-4 h-4 text-indigo-700" />
              <div className="font-semibold text-sm">Calendrier 2025 — Concours communs</div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-0">
              <div className="p-4 border-b md:border-b-0 md:border-r">
                <div className="text-xs text-gray-500">Inscriptions</div>
                <div className="text-sm font-medium">{catalog.calendar_2025.registration_open} → {catalog.calendar_2025.registration_close}</div>
              </div>
              <div className="p-4 border-b md:border-b-0 md:border-r">
                <div className="text-xs text-gray-500">Listes de présélection</div>
                <div className="text-sm font-medium">{catalog.calendar_2025.preselection_lists}</div>
              </div>
              <div className="p-4">
                <div className="text-xs text-gray-500">Écrits et résultats</div>
                <div className="text-sm font-medium">{catalog.calendar_2025.written_exams} · {catalog.calendar_2025.final_results}</div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
