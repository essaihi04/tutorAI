import React, { useState, useRef } from 'react';
import { Volume2, Loader2, AlertCircle } from 'lucide-react';

const TTSTest: React.FC = () => {
  const [text, setText] = useState('');
  const [language, setLanguage] = useState<'fr' | 'ar'>('fr');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const exampleTexts = {
    fr: [
      "Bonjour, bienvenue dans le test de synthèse vocale Darija.",
      "La glycolyse est la première étape de la respiration cellulaire.",
      "Aujourd'hui nous allons étudier la photosynthèse.",
    ],
    ar: [
      "Salam, kidayr? Ghadi ncharhoulek la respiration cellulaire.",
      "Lyoum ghadi ndorou la photosynthèse w la glycolyse.",
      "La mitochondrie hiya l'usine énergétique dial la cellule.",
    ],
  };

  const handleSynthesize = async () => {
    if (!text.trim()) {
      setError('Veuillez entrer du texte');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/tts/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text.trim(),
          language: language,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erreur de synthèse');
      }

      const data = await response.json();

      // Convert base64 to blob and play
      const audioBlob = base64ToBlob(data.audio_base64, data.format);
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setIsLoading(false);
    }
  };

  const base64ToBlob = (base64: string, mimeType: string): Blob => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  };

  const loadExample = (example: string) => {
    setText(example);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🎙️ Test TTS Darija
          </h1>
          <p className="text-gray-600">
            Testez la synthèse vocale avec le modèle Kokoro fine-tuné pour la Darija
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
          {/* Language Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Langue / اللغة
            </label>
            <div className="flex gap-4">
              <button
                onClick={() => setLanguage('fr')}
                className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all ${
                  language === 'fr'
                    ? 'bg-indigo-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Français
              </button>
              <button
                onClick={() => setLanguage('ar')}
                className={`flex-1 py-3 px-6 rounded-lg font-medium transition-all ${
                  language === 'ar'
                    ? 'bg-indigo-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                العربية / Darija
              </button>
            </div>
          </div>

          {/* Text Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Texte à synthétiser
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={
                language === 'fr'
                  ? 'Entrez votre texte en français...'
                  : 'أدخل النص بالعربية أو الدارجة...'
              }
              className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              dir={language === 'ar' ? 'rtl' : 'ltr'}
              maxLength={500}
            />
            <div className="text-right text-sm text-gray-500 mt-1">
              {text.length} / 500 caractères
            </div>
          </div>

          {/* Example Texts */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Exemples
            </label>
            <div className="space-y-2">
              {exampleTexts[language].map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => loadExample(example)}
                  className="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors"
                  dir={language === 'ar' ? 'rtl' : 'ltr'}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="flex items-center gap-2 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Synthesize Button */}
          <button
            onClick={handleSynthesize}
            disabled={isLoading || !text.trim()}
            className="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Synthèse en cours...
              </>
            ) : (
              <>
                <Volume2 className="w-6 h-6" />
                Lire le texte
              </>
            )}
          </button>

          {/* Hidden Audio Element */}
          <audio ref={audioRef} className="hidden" />
        </div>

        {/* Info Card */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">ℹ️ Informations</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Modèle : Kokoro-82M (voix française)</li>
            <li>• Supporte le français et la Darija romanisée</li>
            <li>• Temps de synthèse : ~6-9 secondes par phrase</li>
            <li>• Qualité : 24kHz, 16-bit mono WAV</li>
          </ul>
        </div>

        {/* Tips Card */}
        <div className="mt-4 bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h3 className="font-semibold text-amber-900 mb-2">💡 Conseils pour la Darija</h3>
          <ul className="text-sm text-amber-800 space-y-1">
            <li>• Écrivez la Darija en <strong>lettres latines</strong> (ex: "Salam, kidayr?")</li>
            <li>• Mélangez français et Darija librement (ex: "Ghadi ncharhoulek la photosynthèse")</li>
            <li>• L'arabe pur sera translittéré automatiquement mais la prononciation sera approximative</li>
            <li>• Pour une meilleure prononciation, utilisez la romanisation Darija</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default TTSTest;
