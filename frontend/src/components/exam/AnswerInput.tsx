import { useState, useRef } from 'react';
import { Loader2, Camera, Type, Check, X, Sparkles, PenLine, ImageIcon, PenTool, Calculator, FileText, AlertCircle } from 'lucide-react';
import DrawingCanvas from './DrawingCanvas';
import LatexRenderer from './LatexRenderer';
import { extractTextFromImage } from '../../services/api';

interface Choice {
  letter: string;
  text: string;
}

interface Props {
  questionContent: string;
  questionType?: 'open' | 'qcm' | 'vrai_faux' | 'association' | 'schema';
  choices?: Choice[];
  itemsLeft?: string[];
  itemsRight?: string[];
  value: string;
  onChange: (value: string) => void;
  onImageChange?: (imageBase64: string | null) => void;
  onSubmit?: () => void;
  submitting?: boolean;
  disabled?: boolean;
  placeholder?: string;
  showCorrection?: boolean;
  correctAnswer?: string | boolean;
  subject?: string;
}

/* ---- Math symbol groups ---- */
const MATH_GROUPS = [
  {
    label: 'Opérateurs',
    symbols: [
      { display: '±', insert: '±' },
      { display: '×', insert: '×' },
      { display: '÷', insert: '÷' },
      { display: '√', insert: '√(' },
      { display: '∞', insert: '∞' },
      { display: '≈', insert: '≈' },
      { display: '≠', insert: '≠' },
      { display: '≤', insert: '≤' },
      { display: '≥', insert: '≥' },
    ],
  },
  {
    label: 'Exposants',
    symbols: [
      { display: 'x²', insert: '²' },
      { display: 'x³', insert: '³' },
      { display: 'xⁿ', insert: '^n' },
      { display: 'x⁻¹', insert: '⁻¹' },
      { display: '½', insert: '½' },
      { display: '⅓', insert: '⅓' },
    ],
  },
  {
    label: 'Lettres grecques',
    symbols: [
      { display: 'α', insert: 'α' },
      { display: 'β', insert: 'β' },
      { display: 'γ', insert: 'γ' },
      { display: 'δ', insert: 'δ' },
      { display: 'Δ', insert: 'Δ' },
      { display: 'θ', insert: 'θ' },
      { display: 'λ', insert: 'λ' },
      { display: 'μ', insert: 'μ' },
      { display: 'π', insert: 'π' },
      { display: 'σ', insert: 'σ' },
      { display: 'ω', insert: 'ω' },
      { display: 'Ω', insert: 'Ω' },
    ],
  },
  {
    label: 'Physique / Chimie',
    symbols: [
      { display: '→', insert: '→' },
      { display: '⇌', insert: '⇌' },
      { display: '°C', insert: '°C' },
      { display: 'mol/L', insert: 'mol·L⁻¹' },
      { display: 'm/s', insert: 'm·s⁻¹' },
      { display: 'J/mol', insert: 'J·mol⁻¹' },
      { display: 'N', insert: 'N' },
      { display: 'Pa', insert: 'Pa' },
      { display: 'eV', insert: 'eV' },
    ],
  },
  {
    label: 'Fonctions',
    symbols: [
      { display: 'sin', insert: 'sin(' },
      { display: 'cos', insert: 'cos(' },
      { display: 'tan', insert: 'tan(' },
      { display: 'ln', insert: 'ln(' },
      { display: 'log', insert: 'log(' },
      { display: 'exp', insert: 'exp(' },
      { display: 'lim', insert: 'lim ' },
      { display: '∫', insert: '∫' },
      { display: 'Σ', insert: 'Σ' },
      { display: 'd/dx', insert: 'd/dx' },
    ],
  },
];

type InputMode = 'text' | 'draw' | 'photo';

export default function AnswerInput({
  questionContent,
  questionType = 'open',
  choices: choicesProp = [],
  itemsLeft: itemsLeftProp = [],
  itemsRight: itemsRightProp = [],
  value: valueProp,
  onChange,
  onImageChange,
  onSubmit,
  submitting = false,
  disabled = false,
  placeholder = 'Écrivez votre réponse ici...',
  showCorrection = false,
  correctAnswer,
  subject = '',
}: Props) {
  // Defensive coercion: default-parameter only fires on `undefined`, NOT on
  // `null`. The exam API can send `choices: null` / `items_left: null` on an
  // open question, and `answers[qKey]` may momentarily be null when the
  // panel switches exercise/question — calling `.length` / `.trim()` on
  // those would crash the whole session with "Cannot read properties of
  // null (reading 'length')".
  const choices = Array.isArray(choicesProp) ? choicesProp : [];
  const itemsLeft = Array.isArray(itemsLeftProp) ? itemsLeftProp : [];
  const itemsRight = Array.isArray(itemsRightProp) ? itemsRightProp : [];
  const value = typeof valueProp === 'string' ? valueProp : '';
  const detectedType = questionType !== 'open' ? questionType : detectQuestionType(questionContent || '');
  const needsMath = detectedType === 'calcul' || detectedType === 'definition';
  const needsDraw = detectedType === 'graphe' || detectedType === 'schema';
  const defaultMode: InputMode = needsDraw ? 'draw' : 'text';
  const [inputMode, setInputMode] = useState<InputMode>(defaultMode);
  const [showMathPanel, setShowMathPanel] = useState(false);
  const [drawingDataUrl, setDrawingDataUrl] = useState<string>('');
  const [photoPreview, setPhotoPreview] = useState<string | null>(null);
  const [extracting, setExtracting] = useState(false);
  const [extractionError, setExtractionError] = useState<string | null>(null);
  const [extractedFromImage, setExtractedFromImage] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const insertSymbol = (symbol: string) => {
    const ta = textareaRef.current;
    if (!ta) { onChange(value + symbol); return; }
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const newValue = value.substring(0, start) + symbol + value.substring(end);
    onChange(newValue);
    requestAnimationFrame(() => {
      ta.focus();
      const pos = start + symbol.length;
      ta.setSelectionRange(pos, pos);
    });
  };

  const handleDrawingChange = (dataUrl: string) => {
    setDrawingDataUrl(dataUrl);
    if (dataUrl) {
      onChange('[Dessin: courbe/schéma tracé sur le canvas]');
      onImageChange?.(dataUrl);
    } else {
      onChange('');
      onImageChange?.(null);
    }
  };

  // Extract text from photo using Vision AI
  const handlePhotoExtraction = async (base64: string) => {
    setExtracting(true);
    setExtractionError(null);
    try {
      const res = await extractTextFromImage(base64, questionContent, subject);
      const data = res.data;
      
      // Check if there was an error from the API
      if (data.error) {
        console.warn('Extraction API error:', data.error);
        setExtractionError("Extraction automatique indisponible. Vous pouvez saisir votre réponse manuellement.");
        return;
      }
      
      const extracted = data.extracted_text || '';
      if (extracted && extracted.trim()) {
        onChange(extracted);
        setExtractedFromImage(true);
        // Switch to text mode to show extracted text
        setInputMode('text');
      } else {
        setExtractionError("Aucun texte détecté dans l'image. Vous pouvez saisir votre réponse manuellement.");
      }
    } catch (err: any) {
      console.error('Extraction failed:', err);
      setExtractionError("Erreur lors de l'extraction. Vous pouvez saisir votre réponse manuellement.");
    } finally {
      setExtracting(false);
    }
  };

  const hasContent = !!(value?.trim() || drawingDataUrl || photoPreview);

  const SubmitButton = ({ extraClass = '' }: { extraClass?: string }) => (
    onSubmit && !showCorrection ? (
      <div className={`px-4 pb-4 ${extraClass}`}>
        <button
          onClick={onSubmit}
          disabled={disabled || submitting || !hasContent}
          className="group w-full relative flex items-center justify-center gap-2.5 px-6 py-3.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-xl font-bold text-sm hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 disabled:from-slate-300 disabled:via-slate-300 disabled:to-slate-300 disabled:cursor-not-allowed transition-all shadow-lg shadow-indigo-500/25 hover:shadow-xl hover:shadow-indigo-500/40 disabled:shadow-none overflow-hidden"
        >
          {/* Shimmer effect on hover */}
          {hasContent && !submitting && (
            <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700" />
          )}
          {submitting ? (
            <><Loader2 className="w-4 h-4 animate-spin relative" /> <span className="relative">{photoPreview || drawingDataUrl ? 'Analyse IA en cours...' : 'Évaluation IA...'}</span></>
          ) : (
            <>
              <Sparkles className="w-4 h-4 group-hover:rotate-12 group-hover:scale-110 transition-transform relative" />
              <span className="relative">{photoPreview || drawingDataUrl ? 'Analyser ma photo' : 'Vérifier ma réponse'}</span>
              {hasContent && (
                <span className="hidden sm:inline-flex items-center gap-1 ml-1 px-1.5 py-0.5 bg-white/20 rounded text-[10px] font-mono opacity-80 relative">
                  Ctrl+↵
                </span>
              )}
            </>
          )}
        </button>
      </div>
    ) : null
  );

  // Keyboard shortcut: Ctrl+Enter to submit
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && hasContent && !submitting && !disabled && onSubmit) {
      e.preventDefault();
      onSubmit();
    }
  };

  // QCM with clickable choices
  if (detectedType === 'qcm' && choices.length > 0) {
    return (
      <div className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
        <div className="px-4 pt-4 pb-2">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-6 h-6 rounded-lg bg-violet-100 flex items-center justify-center">
              <PenLine className="w-3 h-3 text-violet-600" />
            </div>
            <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Sélectionnez la bonne réponse</p>
          </div>
          <div className="space-y-2">
            {choices.map((choice) => {
              const isSelected = value === choice.letter;
              const isCorrect = correctAnswer === choice.letter;

              return (
                <button
                  key={choice.letter}
                  onClick={() => !disabled && onChange(choice.letter)}
                  disabled={disabled}
                  className={`w-full text-left p-3.5 rounded-xl border-2 transition-all flex items-center gap-3 ${
                    isSelected
                      ? showCorrection
                        ? isCorrect
                          ? 'border-emerald-400 bg-emerald-50/80 shadow-sm shadow-emerald-500/10'
                          : 'border-red-400 bg-red-50/80 shadow-sm shadow-red-500/10'
                        : 'border-blue-400 bg-blue-50/80 shadow-sm shadow-blue-500/10'
                      : showCorrection && isCorrect
                        ? 'border-emerald-400 bg-emerald-50/80'
                        : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/80'
                  } ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  <span className={`w-8 h-8 rounded-xl flex items-center justify-center text-sm font-bold transition-all ${
                    isSelected
                      ? showCorrection
                        ? isCorrect ? 'bg-emerald-500 text-white shadow-sm' : 'bg-red-500 text-white shadow-sm'
                        : 'bg-blue-600 text-white shadow-sm'
                      : showCorrection && isCorrect
                        ? 'bg-emerald-500 text-white'
                        : 'bg-slate-100 text-slate-500'
                  }`}>
                    {showCorrection && isSelected ? (
                      isCorrect ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />
                    ) : showCorrection && isCorrect ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      choice.letter.toUpperCase()
                    )}
                  </span>
                  <LatexRenderer as="span" className={`flex-1 text-[13px] leading-relaxed ${
                    isSelected ? 'font-medium text-slate-800' : 'text-slate-600'
                  }`}>{choice.text}</LatexRenderer>
                </button>
              );
            })}
          </div>
        </div>
        <SubmitButton extraClass="pt-2" />
      </div>
    );
  }

  // Vrai/Faux with toggle buttons
  if (detectedType === 'vrai_faux') {
    const isTrue = value === 'vrai';
    const isFalse = value === 'faux';
    const correctBool = correctAnswer === true || correctAnswer === 'vrai';

    return (
      <div className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
        <div className="px-4 pt-4 pb-2">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-6 h-6 rounded-lg bg-amber-100 flex items-center justify-center">
              <PenLine className="w-3 h-3 text-amber-600" />
            </div>
            <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Cette affirmation est-elle vraie ou fausse ?</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => !disabled && onChange('vrai')}
              disabled={disabled}
              className={`flex-1 py-3.5 px-5 rounded-xl border-2 font-semibold text-sm transition-all flex items-center justify-center gap-2.5 ${
                isTrue
                  ? showCorrection
                    ? correctBool
                      ? 'border-emerald-400 bg-emerald-50 text-emerald-700 shadow-sm shadow-emerald-500/10'
                      : 'border-red-400 bg-red-50 text-red-700 shadow-sm shadow-red-500/10'
                    : 'border-blue-400 bg-blue-50 text-blue-700 shadow-sm shadow-blue-500/10'
                  : showCorrection && correctBool
                    ? 'border-emerald-400 bg-emerald-50 text-emerald-700'
                    : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-600'
              } ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {showCorrection && isTrue && (correctBool ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />)}
              {showCorrection && !isTrue && correctBool && <Check className="w-4 h-4" />}
              Vrai
            </button>
            <button
              onClick={() => !disabled && onChange('faux')}
              disabled={disabled}
              className={`flex-1 py-3.5 px-5 rounded-xl border-2 font-semibold text-sm transition-all flex items-center justify-center gap-2.5 ${
                isFalse
                  ? showCorrection
                    ? !correctBool
                      ? 'border-emerald-400 bg-emerald-50 text-emerald-700 shadow-sm shadow-emerald-500/10'
                      : 'border-red-400 bg-red-50 text-red-700 shadow-sm shadow-red-500/10'
                    : 'border-blue-400 bg-blue-50 text-blue-700 shadow-sm shadow-blue-500/10'
                  : showCorrection && !correctBool
                    ? 'border-emerald-400 bg-emerald-50 text-emerald-700'
                    : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-600'
              } ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
            >
              {showCorrection && isFalse && (!correctBool ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />)}
              {showCorrection && !isFalse && !correctBool && <Check className="w-4 h-4" />}
              Faux
            </button>
          </div>
        </div>
        <SubmitButton extraClass="pt-2" />
      </div>
    );
  }

  // Association with interactive clickable matching
  if (detectedType === 'association' || (questionType === 'association' && itemsLeft.length > 0)) {
    const leftItems = itemsLeft.length > 0 ? itemsLeft : ['1', '2', '3', '4'];
    const rightItems = itemsRight.length > 0 ? itemsRight : ['a', 'b', 'c', 'd'];
    
    // Parse current value to get existing pairs
    const existingPairs: Record<string, string> = {};
    if (value) {
      // Match patterns like (1,a) or 1-a or 1,a (supports any letter a-z)
      const pairMatches = value.match(/\(?(\d+)[,\-)]([a-z])\)?/gi);
      if (pairMatches) {
        pairMatches.forEach(match => {
          const nums = match.match(/(\d+)/);
          const letter = match.match(/([a-z])/i);
          if (nums && letter) {
            existingPairs[nums[1]] = letter[1].toLowerCase();
          }
        });
      }
    }
    
    const handleLeftClick = (leftNum: string) => {
      if (disabled) return;
      setSelectedLeft(selectedLeft === leftNum ? null : leftNum);
    };
    
    const handleRightClick = (rightLetter: string) => {
      if (disabled || !selectedLeft) return;
      
      // Create or update pair
      const newPairs = { ...existingPairs, [selectedLeft]: rightLetter };
      
      // Convert to string format
      const pairs = Object.entries(newPairs)
        .sort(([a], [b]) => parseInt(a) - parseInt(b))
        .map(([num, letter]) => `(${num},${letter})`)
        .join(' ');
      
      onChange(pairs);
      setSelectedLeft(null);
    };
    
    const clearPair = (leftNum: string) => {
      if (disabled) return;
      const newPairs = { ...existingPairs };
      delete newPairs[leftNum];
      
      const pairs = Object.entries(newPairs)
        .sort(([a], [b]) => parseInt(a) - parseInt(b))
        .map(([num, letter]) => `(${num},${letter})`)
        .join(' ');
      
      onChange(pairs);
    };
    
    // Get paired status for right items
    const pairedRightLetters = Object.values(existingPairs);
    
    return (
      <div className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
        <div className="px-4 pt-4 pb-4">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-6 h-6 rounded-lg bg-purple-100 flex items-center justify-center">
              <PenLine className="w-3 h-3 text-purple-600" />
            </div>
            <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Reliez les éléments</p>
          </div>
          
          {/* Instructions */}
          <div className="bg-blue-50 border border-blue-100 rounded-lg p-2.5 mb-4">
            <p className="text-[11px] text-blue-700">
              <span className="font-semibold">Comment faire :</span> Cliquez sur un numéro du <span className="font-medium text-purple-700">Groupe 1</span>, puis cliquez sur une lettre du <span className="font-medium text-amber-700">Groupe 2</span> pour créer une paire.
            </p>
          </div>
          
          {/* Two columns display */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            {/* Left column */}
            <div className="bg-slate-50 rounded-xl p-3">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Groupe 1</p>
              <div className="space-y-2">
                {leftItems.map((item, idx) => {
                  const num = String(idx + 1);
                  const isSelected = selectedLeft === num;
                  const isPaired = existingPairs[num];
                  
                  return (
                    <button
                      key={idx}
                      onClick={() => handleLeftClick(num)}
                      disabled={disabled}
                      className={`w-full flex items-center gap-2 px-3 py-2.5 rounded-lg border-2 transition-all text-left ${
                        isSelected
                          ? 'border-purple-500 bg-purple-100 shadow-sm'
                          : isPaired
                          ? 'border-emerald-400 bg-emerald-50'
                          : 'border-slate-200 bg-white hover:border-purple-300 hover:bg-purple-50/50'
                      } ${disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'}`}
                    >
                      <span className={`w-6 h-6 rounded flex items-center justify-center text-[11px] font-bold ${
                        isSelected
                          ? 'bg-purple-500 text-white'
                          : isPaired
                          ? 'bg-emerald-500 text-white'
                          : 'bg-purple-100 text-purple-700'
                      }`}>
                        {isPaired ? <Check className="w-3.5 h-3.5" /> : num}
                      </span>
                      <LatexRenderer as="span" className="text-xs text-slate-700 flex-1">{item}</LatexRenderer>
                      {isPaired && (
                        <span className="text-[10px] font-bold text-emerald-600 bg-emerald-100 px-1.5 py-0.5 rounded">
                          → {isPaired.toUpperCase()}
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
            
            {/* Right column */}
            <div className="bg-slate-50 rounded-xl p-3">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Groupe 2</p>
              <div className="space-y-2">
                {rightItems.map((item, idx) => {
                  const letter = String.fromCharCode(97 + idx);
                  const isPaired = pairedRightLetters.includes(letter);
                  const isActive = selectedLeft && !isPaired;
                  
                  return (
                    <button
                      key={idx}
                      onClick={() => handleRightClick(letter)}
                      disabled={disabled || !selectedLeft || isPaired}
                      className={`w-full flex items-center gap-2 px-3 py-2.5 rounded-lg border-2 transition-all text-left ${
                        isPaired
                          ? 'border-emerald-400 bg-emerald-50 opacity-70'
                          : isActive
                          ? 'border-amber-400 bg-amber-50 hover:border-amber-500 hover:bg-amber-100 cursor-pointer shadow-sm'
                          : 'border-slate-200 bg-white opacity-50 cursor-not-allowed'
                      }`}
                    >
                      <span className={`w-6 h-6 rounded flex items-center justify-center text-[11px] font-bold ${
                        isPaired
                          ? 'bg-emerald-500 text-white'
                          : isActive
                          ? 'bg-amber-400 text-white animate-pulse'
                          : 'bg-amber-100 text-amber-700'
                      }`}>
                        {isPaired ? <Check className="w-3.5 h-3.5" /> : letter}
                      </span>
                      <LatexRenderer as="span" className="text-xs text-slate-700 flex-1">{item}</LatexRenderer>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
          
          {/* Current pairs display */}
          {Object.keys(existingPairs).length > 0 && (
            <div className="bg-slate-50 rounded-xl p-3 mb-4">
              <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">Vos associations</p>
              <div className="flex flex-wrap gap-2">
                {Object.entries(existingPairs)
                  .sort(([a], [b]) => parseInt(a) - parseInt(b))
                  .map(([num, letter]) => (
                    <button
                      key={num}
                      onClick={() => clearPair(num)}
                      disabled={disabled}
                      className="flex items-center gap-1.5 px-2.5 py-1.5 bg-emerald-100 text-emerald-700 rounded-lg text-xs font-medium hover:bg-red-100 hover:text-red-600 transition-colors"
                    >
                      <span>({num},{letter})</span>
                      <X className="w-3 h-3" />
                    </button>
                  ))}
              </div>
              <p className="text-[10px] text-slate-400 mt-2">Cliquez sur une paire pour la supprimer</p>
            </div>
          )}
          
          {/* Hidden input for form submission */}
          <input type="hidden" value={value} />
        </div>
        <SubmitButton extraClass="pt-2" />
      </div>
    );
  }

  // Open answer with tabs: Texte / Dessin / Photo
  const modes: { key: InputMode; icon: React.ReactNode; label: string; hint: string; accent: string }[] = [
    { key: 'text',  icon: <Type className="w-3.5 h-3.5" />,    label: 'Texte',  hint: 'Rédigez votre réponse',         accent: 'from-blue-500 to-indigo-600' },
    { key: 'draw',  icon: <PenTool className="w-3.5 h-3.5" />, label: 'Dessin', hint: 'Tracez courbes et schémas',     accent: 'from-emerald-500 to-teal-600' },
    { key: 'photo', icon: <Camera className="w-3.5 h-3.5" />,  label: 'Photo',  hint: 'Photographiez votre brouillon', accent: 'from-amber-500 to-orange-600' },
  ];

  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-sm">
      {/* Mode tabs — pill-style with per-mode color accent */}
      <div className="flex items-center gap-1.5 px-3 py-2.5 border-b border-slate-100 bg-gradient-to-r from-slate-50/80 via-white to-slate-50/80">
        {modes.map((m) => {
          const active = inputMode === m.key;
          return (
            <button
              key={m.key}
              onClick={() => setInputMode(m.key)}
              title={m.hint}
              className={`relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                active
                  ? `bg-gradient-to-br ${m.accent} text-white shadow-md scale-105`
                  : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100/70'
              }`}
            >
              {m.icon}
              <span>{m.label}</span>
            </button>
          );
        })}

        {/* Math toolbar toggle for text mode */}
        {inputMode === 'text' && (
          <button
            onClick={() => setShowMathPanel((p) => !p)}
            title="Symboles mathématiques"
            className={`ml-auto flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
              showMathPanel
                ? 'bg-gradient-to-br from-violet-500 to-purple-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-violet-600 hover:bg-violet-50'
            }`}
          >
            <Calculator className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">∑ Symboles</span>
          </button>
        )}

        {/* Hint for current mode */}
        {inputMode !== 'text' && (
          <span className="ml-auto text-[10px] text-slate-400 px-2 hidden sm:inline italic">
            {inputMode === 'draw' && '✏️ Tracez directement sur le canvas'}
            {inputMode === 'photo' && '📸 Photo manuscrite + OCR automatique'}
          </span>
        )}
      </div>

      {/* Math symbol panel */}
      {inputMode === 'text' && showMathPanel && (
        <div className="border-b border-slate-100 bg-gradient-to-br from-violet-50/50 to-white px-3 py-3 space-y-2.5 max-h-[200px] overflow-y-auto">
          {MATH_GROUPS.map((group) => (
            <div key={group.label}>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">{group.label}</p>
              <div className="flex flex-wrap gap-1">
                {group.symbols.map((sym) => (
                  <button
                    key={sym.display}
                    onClick={() => insertSymbol(sym.insert)}
                    title={`Insérer ${sym.display}`}
                    className="min-w-[32px] h-8 px-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-violet-50 hover:border-violet-300 hover:text-violet-700 active:scale-95 transition-all shadow-sm"
                  >
                    {sym.display}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Text input */}
      {inputMode === 'text' && (
        <div className="p-4">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={needsMath ? 'Écrivez votre réponse… Utilisez les symboles ci-dessus pour les formules' : placeholder}
            rows={6}
            className="w-full min-h-[160px] bg-white text-slate-900 border border-slate-200 rounded-xl px-4 py-3 text-[14px] leading-[1.7] resize-y focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-400 disabled:bg-slate-50 disabled:text-slate-400 placeholder:text-slate-400 transition-all"
          />
          {/* Char counter + encouragement */}
          <div className="mt-2 flex items-center justify-between gap-3 text-[11px]">
            <div className="flex items-center gap-2">
              {needsMath && !showMathPanel && (
                <button
                  onClick={() => setShowMathPanel(true)}
                  className="text-violet-500 hover:text-violet-700 font-semibold flex items-center gap-1"
                >
                  <Calculator className="w-3 h-3" /> Ouvrir les symboles maths
                </button>
              )}
            </div>
            <div className="flex items-center gap-2 text-slate-400">
              {value.trim().length > 0 && (
                <span className={`font-mono ${value.trim().length < 20 ? 'text-amber-500' : value.trim().length < 80 ? 'text-blue-500' : 'text-emerald-500'}`}>
                  {value.trim().length < 20 ? '✍️' : value.trim().length < 80 ? '💪' : '🔥'} {value.trim().length} car.
                </span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Drawing canvas */}
      {inputMode === 'draw' && (
        <div className="p-4">
          <DrawingCanvas
            showGrid={detectedType === 'graphe'}
            showAxes={detectedType === 'graphe'}
            disabled={disabled}
            onDrawingChange={handleDrawingChange}
          />
          {/* Optional text description alongside drawing */}
          <div className="mt-3">
            <textarea
              value={value.startsWith('[Dessin') ? '' : value}
              onChange={(e) => {
                const desc = e.target.value.trim();
                if (drawingDataUrl) {
                  onChange(desc ? `[Dessin: courbe/schéma tracé]\n${desc}` : '[Dessin: courbe/schéma tracé sur le canvas]');
                } else {
                  onChange(desc);
                }
              }}
              disabled={disabled}
              placeholder="Ajoutez une description ou légende à votre dessin (optionnel)..."
              rows={2}
              className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-[13px] leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-400 disabled:bg-slate-50 disabled:text-slate-400 placeholder:text-slate-500 transition-all"
            />
          </div>
        </div>
      )}

      {/* Photo input */}
      {inputMode === 'photo' && (
        <div className="p-4">
          {extracting ? (
            <div className="border-2 border-dashed border-blue-200 rounded-2xl p-6 text-center bg-blue-50/50">
              <Loader2 className="w-8 h-8 text-blue-500 animate-spin mx-auto mb-3" />
              <p className="text-sm font-medium text-blue-600">Extraction du texte en cours...</p>
              <p className="text-xs text-blue-400 mt-1">Analyse de l'image par IA</p>
            </div>
          ) : photoPreview ? (
            <div className="space-y-3">
              <div className="relative rounded-xl overflow-hidden border border-slate-200">
                <img src={photoPreview} alt="Réponse photo" className="w-full max-h-[200px] object-contain bg-slate-50" />
                {!disabled && (
                  <button
                    onClick={() => { 
                      setPhotoPreview(null); 
                      onImageChange?.(null); 
                      onChange(''); 
                      setExtractedFromImage(false);
                      setExtractionError(null);
                    }}
                    className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors shadow-md"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              
              {/* Extraction error message */}
              {extractionError && (
                <div className="flex items-start gap-2 p-2 bg-amber-50 border border-amber-200 rounded-lg">
                  <AlertCircle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-amber-700">{extractionError}</p>
                </div>
              )}
              
              {/* Success message with extracted text indicator */}
              {extractedFromImage && !extractionError && (
                <div className="flex items-start gap-2 p-2 bg-emerald-50 border border-emerald-200 rounded-lg">
                  <FileText className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-xs text-emerald-700 font-medium">Texte extrait de l'image</p>
                    <p className="text-[10px] text-emerald-600 mt-0.5">Vérifiez et corrigez si nécessaire dans l'onglet "Texte"</p>
                  </div>
                </div>
              )}
              
              {!extractedFromImage && !extractionError && (
                <p className="text-xs text-emerald-600 font-medium flex items-center gap-1.5">
                  <Check className="w-3.5 h-3.5" /> Photo prête — cliquez sur "Vérifier" pour l'analyser par IA
                </p>
              )}
            </div>
          ) : (
            <div className="border-2 border-dashed border-slate-200 rounded-2xl p-6 text-center bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-3">
                <ImageIcon className="w-5 h-5 text-slate-400" />
              </div>
              <p className="text-sm font-medium text-slate-600 mb-1">Prenez en photo votre réponse</p>
              <p className="text-xs text-slate-400 mb-4">Courbes, schémas, tableaux, calculs manuscrits</p>
              <label className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-semibold rounded-xl cursor-pointer hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md shadow-blue-500/20">
                <Camera className="w-4 h-4" />
                Choisir une photo
                <input
                  type="file"
                  accept="image/*"
                  capture="environment"
                  className="hidden"
                  disabled={disabled}
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (!file) return;
                    const reader = new FileReader();
                    reader.onload = async () => {
                      const base64 = reader.result as string;
                      setPhotoPreview(base64);
                      onImageChange?.(base64);
                      // Auto-extract text from the image
                      await handlePhotoExtraction(base64);
                    };
                    reader.readAsDataURL(file);
                  }}
                />
              </label>
              <p className="text-[10px] text-slate-400 mt-3">
                📝 Le texte sera automatiquement extrait et affiché pour vérification
              </p>
            </div>
          )}
        </div>
      )}

      {/* Submit button */}
      <SubmitButton />
    </div>
  );
}

type QuestionType = 'qcm' | 'vrai_faux' | 'association' | 'definition' | 'calcul' | 'tableau' | 'graphe' | 'schema' | null;

function detectQuestionType(content: string): QuestionType {
  const lower = content.toLowerCase();
  if (/\ba\.\s|b\.\s|c\.\s|d\./.test(content) || /suggestion.*correcte/i.test(content)) return 'qcm';
  if (/vrai.*faux|« vrai »|« faux »/i.test(content)) return 'vrai_faux';
  if (/défini[sz]sez|définition/i.test(content)) return 'definition';
  if (/calcul|détermin|résoud|équation|formule/i.test(lower)) return 'calcul';
  if (/tableau|échiquier|grille/i.test(lower)) return 'tableau';
  if (/trac|courbe|graph|représent.*graphi/i.test(lower)) return 'graphe';
  if (/schéma|légende|identifi.*élément/i.test(lower)) return 'schema';
  if (/reliez|groupe 1|groupe 2|associez|correspondance/i.test(lower)) return 'association';
  return null;
}
