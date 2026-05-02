import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles, ArrowRight, Check, X, RotateCw, Trophy,
  Target, AlertCircle, TrendingUp, Brain,
} from 'lucide-react';

/* ════════════════════════════════════════════════════════════
   QUICK DIAGNOSTIC — démo anonyme sans inscription
   3 questions QCM par filière (SVT ou PC) → score + reco + CTA
   ════════════════════════════════════════════════════════════ */

type Filiere = 'svt' | 'pc';

interface Question {
  text: string;
  choices: string[];
  correctIndex: number;
  explanation: string;
  chapter: string;
}

const QUESTIONS: Record<Filiere, Question[]> = {
  svt: [
    {
      text: 'Où se déroule le cycle de Krebs dans la cellule ?',
      choices: [
        'Dans le cytoplasme',
        'Dans le noyau',
        'Dans la matrice mitochondriale',
        'Dans la membrane plasmique',
      ],
      correctIndex: 2,
      explanation: 'Le cycle de Krebs se déroule dans la matrice mitochondriale. Toutes ses enzymes y sont solubles, sauf la succinate déshydrogénase qui est ancrée dans la membrane interne (complexe II).',
      chapter: 'Consommation de la matière organique',
    },
    {
      text: 'Dans un dihybridisme avec deux gènes indépendants, le rapport phénotypique observé en F2 (croisement de F1×F1) est :',
      choices: [
        '3 : 1',
        '1 : 1',
        '9 : 3 : 3 : 1',
        '1 : 2 : 1',
      ],
      correctIndex: 2,
      explanation: 'Pour deux gènes indépendants en F2, le rapport phénotypique est 9:3:3:1 — c\'est la loi de la ségrégation indépendante de Mendel. Maîtriser ce rapport est ESSENTIEL pour le BAC SVT 2026.',
      chapter: 'Génétique — transmission',
    },
    {
      text: 'Le métamorphisme HP-BT (haute pression, basse température) caractérise principalement :',
      choices: [
        'Les zones de collision continentale',
        'Les zones de subduction',
        'Les rifts continentaux',
        'Les zones de volcanisme intra-plaque',
      ],
      correctIndex: 1,
      explanation: 'Le métamorphisme HP-BT (schistes bleus, éclogites avec glaucophane) est la signature des zones de subduction : la plaque plongeante reste froide tout en étant soumise à de fortes pressions.',
      chapter: 'Géologie — subduction',
    },
  ],
  pc: [
    {
      text: 'Lors du dosage d\'un acide faible par une base forte, le pH à l\'équivalence est :',
      choices: [
        'pH = 7',
        'pH > 7',
        'pH < 7',
        'pH = pKa',
      ],
      correctIndex: 1,
      explanation: 'À l\'équivalence d\'un dosage acide faible / base forte, la solution contient uniquement la base conjuguée (faible) qui réagit avec l\'eau pour libérer des ions HO⁻ → pH > 7.',
      chapter: 'Chimie — dosages acide-base',
    },
    {
      text: 'La période propre d\'un dipôle RLC en oscillations libres non amorties est :',
      choices: [
        'T₀ = 2π√(LC)',
        'T₀ = √(LC)',
        'T₀ = LC',
        'T₀ = 1/(2π√(LC))',
      ],
      correctIndex: 0,
      explanation: 'La période propre d\'un dipôle RLC est T₀ = 2π√(LC). Cette formule, et son équivalent fréquentiel f₀ = 1/(2π√(LC)), tombent presque tous les ans au BAC PC.',
      chapter: 'Électricité — RLC',
    },
    {
      text: 'La loi de décroissance radioactive d\'un noyau s\'écrit N(t) = N₀ × e^(-λt). Que représente λ ?',
      choices: [
        'La demi-vie',
        'La constante radioactive (probabilité de désintégration par unité de temps)',
        'Le nombre de noyaux initiaux',
        'L\'activité de la source',
      ],
      correctIndex: 1,
      explanation: 'λ est la constante radioactive (en s⁻¹). Elle est liée à la demi-vie par t₁/₂ = ln(2)/λ. La radioactivité étant probabiliste, λ représente la probabilité par unité de temps qu\'un noyau se désintègre.',
      chapter: 'Nucléaire — radioactivité',
    },
  ],
};

export default function QuickDiagnostic() {
  const [step, setStep] = useState<'choose' | 'quiz' | 'result'>('choose');
  const [filiere, setFiliere] = useState<Filiere>('svt');
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [selectedChoice, setSelectedChoice] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);

  const questions = QUESTIONS[filiere];
  const score = answers.filter((ans, i) => ans === questions[i]?.correctIndex).length;
  const total = questions.length;

  const startQuiz = (f: Filiere) => {
    setFiliere(f);
    setStep('quiz');
    setCurrentQ(0);
    setAnswers([]);
    setSelectedChoice(null);
    setShowFeedback(false);
  };

  const submitAnswer = () => {
    if (selectedChoice === null) return;
    const newAnswers = [...answers, selectedChoice];
    setAnswers(newAnswers);
    setShowFeedback(true);
  };

  const nextQuestion = () => {
    setShowFeedback(false);
    setSelectedChoice(null);
    if (currentQ + 1 >= questions.length) {
      setStep('result');
    } else {
      setCurrentQ(currentQ + 1);
    }
  };

  const restart = () => {
    setStep('choose');
    setCurrentQ(0);
    setAnswers([]);
    setSelectedChoice(null);
    setShowFeedback(false);
  };

  return (
    <section
      id="diagnostic"
      className="relative py-20 sm:py-28 z-10 scroll-mt-20"
    >
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass mb-4 text-xs">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-emerald-200">Démo gratuite · 30 secondes · sans inscription</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight mb-4">
            Teste ton niveau{' '}
            <span className="gradient-text">BAC 2026</span> en 30 secondes
          </h2>
          <p className="text-white/60 text-base sm:text-lg max-w-2xl mx-auto">
            3 questions du niveau examen national. Découvre ce qui te bloque encore et reçois une recommandation personnalisée — le tout sans créer de compte.
          </p>
        </div>

        <div className="rounded-3xl glass border border-white/10 p-6 sm:p-10 shadow-2xl shadow-indigo-500/10">

          {/* ─────── ÉTAPE 1 — Choix filière ─────── */}
          {step === 'choose' && (
            <div className="anim-fade-up">
              <div className="text-center mb-8">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center">
                  <Target className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-2">Quelle est ta filière ?</h3>
                <p className="text-sm text-white/60">Choisis ta filière pour adapter les questions</p>
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <button
                  onClick={() => startQuiz('svt')}
                  className="group p-6 rounded-2xl border-2 border-white/10 hover:border-emerald-400/60 bg-white/5 hover:bg-emerald-500/10 transition-all text-left"
                >
                  <div className="text-3xl mb-2">🧬</div>
                  <div className="font-bold text-lg mb-1">2 BAC SVT</div>
                  <div className="text-sm text-white/60 mb-3">Sciences de la Vie et de la Terre</div>
                  <div className="text-xs text-emerald-300 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    Commencer le test <ArrowRight className="w-3 h-3" />
                  </div>
                </button>

                <button
                  onClick={() => startQuiz('pc')}
                  className="group p-6 rounded-2xl border-2 border-white/10 hover:border-indigo-400/60 bg-white/5 hover:bg-indigo-500/10 transition-all text-left"
                >
                  <div className="text-3xl mb-2">⚛️</div>
                  <div className="font-bold text-lg mb-1">2 BAC PC BIOF</div>
                  <div className="text-sm text-white/60 mb-3">Sciences Physiques-Chimiques</div>
                  <div className="text-xs text-indigo-300 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    Commencer le test <ArrowRight className="w-3 h-3" />
                  </div>
                </button>
              </div>
            </div>
          )}

          {/* ─────── ÉTAPE 2 — Quiz ─────── */}
          {step === 'quiz' && (
            <div className="anim-fade-up">
              {/* Progress bar */}
              <div className="flex items-center gap-3 mb-6">
                <div className="flex-1 h-2 rounded-full bg-white/10 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all"
                    style={{ width: `${((currentQ + (showFeedback ? 1 : 0)) / total) * 100}%` }}
                  />
                </div>
                <span className="text-xs font-bold text-white/70 whitespace-nowrap">
                  {currentQ + 1}/{total}
                </span>
              </div>

              <div className="mb-2 text-xs text-indigo-300 font-semibold uppercase tracking-wider">
                {questions[currentQ].chapter}
              </div>
              <h3 className="text-lg sm:text-xl font-bold mb-6 leading-snug">
                {questions[currentQ].text}
              </h3>

              <div className="space-y-3 mb-6">
                {questions[currentQ].choices.map((choice, idx) => {
                  const isCorrect = idx === questions[currentQ].correctIndex;
                  const isSelected = selectedChoice === idx;
                  const showCorrect = showFeedback && isCorrect;
                  const showWrong = showFeedback && isSelected && !isCorrect;

                  return (
                    <button
                      key={idx}
                      onClick={() => !showFeedback && setSelectedChoice(idx)}
                      disabled={showFeedback}
                      className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-center justify-between gap-3 ${
                        showCorrect
                          ? 'border-emerald-400 bg-emerald-500/15 text-white'
                          : showWrong
                          ? 'border-red-400 bg-red-500/15 text-white'
                          : isSelected
                          ? 'border-indigo-400 bg-indigo-500/15 text-white'
                          : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10 text-white/80'
                      }`}
                    >
                      <span className="text-sm sm:text-base">
                        <span className="font-bold mr-2">{String.fromCharCode(65 + idx)}.</span>
                        {choice}
                      </span>
                      {showCorrect && <Check className="w-5 h-5 text-emerald-400 shrink-0" />}
                      {showWrong && <X className="w-5 h-5 text-red-400 shrink-0" />}
                    </button>
                  );
                })}
              </div>

              {/* Feedback explication */}
              {showFeedback && (
                <div className={`mb-6 p-4 rounded-xl border ${
                  selectedChoice === questions[currentQ].correctIndex
                    ? 'border-emerald-400/30 bg-emerald-500/10'
                    : 'border-amber-400/30 bg-amber-500/10'
                }`}>
                  <div className="flex items-start gap-2 mb-2">
                    {selectedChoice === questions[currentQ].correctIndex ? (
                      <>
                        <Check className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                        <span className="font-bold text-emerald-300">Bonne réponse !</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="w-5 h-5 text-amber-400 mt-0.5 shrink-0" />
                        <span className="font-bold text-amber-300">Pas tout à fait…</span>
                      </>
                    )}
                  </div>
                  <p className="text-sm text-white/80 leading-relaxed">
                    {questions[currentQ].explanation}
                  </p>
                </div>
              )}

              <div className="flex justify-end">
                {!showFeedback ? (
                  <button
                    onClick={submitAnswer}
                    disabled={selectedChoice === null}
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-bold disabled:opacity-40 disabled:cursor-not-allowed hover:scale-[1.02] transition-all"
                  >
                    Valider <ArrowRight className="w-4 h-4" />
                  </button>
                ) : (
                  <button
                    onClick={nextQuestion}
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 text-white font-bold hover:scale-[1.02] transition-all"
                  >
                    {currentQ + 1 >= total ? 'Voir mon résultat' : 'Question suivante'}
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          )}

          {/* ─────── ÉTAPE 3 — Résultat ─────── */}
          {step === 'result' && (
            <div className="anim-fade-up text-center">
              <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-amber-400 to-pink-500 flex items-center justify-center">
                <Trophy className="w-10 h-10 text-white" />
              </div>

              <div className="text-5xl sm:text-6xl font-black mb-2">
                <span className="gradient-text">{score}/{total}</span>
              </div>
              <div className="text-lg text-white/70 mb-6">
                {score === total && '🏆 Parfait ! Tu maîtrises ces chapitres clés.'}
                {score === total - 1 && '🎯 Excellent ! Encore quelques détails à peaufiner.'}
                {score === 1 && '📘 Tu connais les bases — il faut consolider.'}
                {score === 0 && '🌱 Pas grave — c\'est exactement pour ça que Moalim existe.'}
                {score > 1 && score < total - 1 && '💪 Bon début ! Avec un peu de coaching ciblé, tu peux atteindre 18/20.'}
              </div>

              {/* Recap par question */}
              <div className="text-left bg-white/5 border border-white/10 rounded-2xl p-5 mb-6">
                <div className="text-xs font-bold uppercase tracking-wider text-white/60 mb-3">
                  Détail de tes réponses
                </div>
                <ul className="space-y-3">
                  {questions.map((q, i) => {
                    const correct = answers[i] === q.correctIndex;
                    return (
                      <li key={i} className="flex items-start gap-3 text-sm">
                        {correct ? (
                          <Check className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
                        ) : (
                          <X className="w-5 h-5 text-red-400 mt-0.5 shrink-0" />
                        )}
                        <div>
                          <div className="font-semibold text-white/90">{q.chapter}</div>
                          <div className="text-xs text-white/55 mt-0.5">{q.text}</div>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              </div>

              {/* CTA inscription */}
              <div className="rounded-2xl bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-300/30 p-6 mb-6">
                <div className="flex items-center justify-center gap-2 mb-3">
                  <Brain className="w-5 h-5 text-indigo-300" />
                  <span className="text-sm font-bold text-indigo-100 uppercase tracking-wider">
                    Recommandation personnalisée
                  </span>
                </div>
                <p className="text-base sm:text-lg text-white/90 mb-5 leading-relaxed">
                  {score === total ? (
                    <>Tu as <b className="text-emerald-300">un excellent niveau de base</b>. Avec Moalim, tu peux passer à la <b>vitesse supérieure</b> : examens blancs aux prédictions BAC 2026, exercices de difficulté croissante, suivi personnalisé pour viser <b className="text-amber-300">la mention Très Bien</b>.</>
                  ) : score >= total - 1 ? (
                    <>Tu es <b className="text-emerald-300">déjà bien préparé·e</b>. Notre IA peut combler les <b>derniers points faibles</b> identifiés ci-dessus en quelques sessions ciblées, pour <b className="text-amber-300">décrocher la mention Bien</b> ou plus.</>
                  ) : score >= 1 ? (
                    <>Tu as <b className="text-amber-300">les bases mais des lacunes ciblées</b>. Notre tuteur IA peut <b>reprendre chaque chapitre</b> identifié ci-dessus à ton rythme, en français, arabe ou darija. Avec 1h/jour pendant 8 semaines, tu peux <b className="text-emerald-300">passer de la moyenne à la mention</b>.</>
                  ) : (
                    <>Pas de panique — <b className="text-amber-300">c'est exactement pour ça que Moalim a été créé</b>. Notre IA reprend les bases avec toi, en français ou darija, et te guide chapitre par chapitre. <b>Beaucoup d'élèves partent de zéro et atteignent la mention</b> en 3 mois de travail régulier.</>
                  )}
                </p>

                <Link
                  to="/inscription"
                  className="inline-flex items-center gap-2 px-7 py-4 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-cyan-500 text-white font-bold text-base shadow-2xl shadow-indigo-500/40 hover:shadow-indigo-500/60 transition-all hover:scale-[1.02]"
                >
                  <Sparkles className="w-5 h-5" />
                  Créer mon compte gratuit
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <div className="text-xs text-white/50 mt-3">
                  ✓ Sans carte bancaire · ✓ Première session offerte · ✓ Annulation libre
                </div>
              </div>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
                <button
                  onClick={restart}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl glass text-white/80 hover:text-white hover:bg-white/10 transition-all text-sm"
                >
                  <RotateCw className="w-4 h-4" />
                  Refaire le test
                </button>
                <a
                  href="/blog/predictions-bac-2026-maroc.html"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl glass text-white/80 hover:text-white hover:bg-white/10 transition-all text-sm"
                >
                  <TrendingUp className="w-4 h-4" />
                  Lire les prédictions BAC 2026
                </a>
              </div>
            </div>
          )}

        </div>
      </div>
    </section>
  );
}
