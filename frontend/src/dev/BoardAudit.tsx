/**
 * Planche de contrôle des TABLEAUX — page de DÉVELOPPEMENT uniquement.
 *
 * Elle monte `AIWhiteboard` dans chacun de ses modes, sans backend ni
 * session. On y vérifie ce qu'un test unitaire ne montre pas : que chaque
 * tableau s'ouvre bien en plein écran, qu'il porte le coin élève avec son
 * micro, et que le bouton ⤡ ramène au cadre de la page.
 *
 * Route : /dev/board-audit (montée seulement quand import.meta.env.DEV).
 */
import { useState } from 'react';
import AIWhiteboard from '../components/session/AIWhiteboard';

type Mode = 'cours' | 'schema' | 'dessin';

const LIGNES_DE_COURS = [
  { type: 'title' as const, content: 'Le dipôle RC' },
  { type: 'text' as const, content: 'La charge d’un condensateur à travers une résistance suit une loi exponentielle.' },
  { type: 'math' as const, content: 'u_C(t) = E\\left(1 - e^{-t/\\tau}\\right)' },
  { type: 'step' as const, content: 'La constante de temps vaut τ = RC, en secondes.' },
  { type: 'note' as const, content: 'À t = 5τ, le condensateur est chargé à 99 %.' },
];

const COMMANDES_DE_DESSIN = [
  {
    title: 'Désintégration α',
    elements: [
      { id: 'noyau', type: 'circle' as const, x: 250, y: 180, radius: 70, color: 'cyan', strokeWidth: 3, label: 'Noyau père' },
      {
        id: 'alpha', type: 'arrow' as const, color: 'orange', strokeWidth: 3, label: 'particule α',
        points: [{ x: 320, y: 180 }, { x: 450, y: 140 }],
      },
      { id: 'legende', type: 'text' as const, x: 250, y: 300, text: 'Le noyau perd 2 protons et 2 neutrons', color: 'white', strokeWidth: 1, fontSize: 16 },
    ],
  },
];

export default function BoardAudit() {
  const [mode, setMode] = useState<Mode>('cours');
  const [envoyes, setEnvoyes] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);

  // Le tableau appelle ce canal comme il appellerait la session : on note ce
  // qui part, et on répond après un instant pour voir la bulle du professeur.
  const recevoirQuestion = (texte: string) => {
    setEnvoyes(liste => [...liste, texte]);
    setBusy(true);
    setTimeout(() => setBusy(false), 900);
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <h1 className="text-2xl font-bold">Planche de contrôle des tableaux</h1>
      <p className="mt-1 text-sm text-slate-400">
        Chaque mode est rendu par le composant réel de la session. Le tableau doit
        s’ouvrir en plein écran et porter le coin élève (✋ Poser une question).
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        {(['cours', 'schema', 'dessin'] as const).map(clef => (
          <button
            key={clef}
            onClick={() => setMode(clef)}
            data-mode={clef}
            className={`rounded-lg px-3 py-1.5 text-sm ${mode === clef ? 'bg-cyan-500 text-slate-950' : 'bg-white/10'}`}
          >
            {clef}
          </button>
        ))}
      </div>

      <p className="mt-3 text-xs text-slate-400" data-questions-envoyees={envoyes.length}>
        Questions parties vers la session : {envoyes.length ? envoyes.join(' | ') : 'aucune'}
      </p>

      <div className="mt-4 h-[70vh] overflow-hidden rounded-xl border border-white/10">
        <AIWhiteboard
          isVisible
          onClose={() => undefined}
          boardContent={mode === 'cours' ? { title: 'Dipôle RC', lines: LIGNES_DE_COURS } : null}
          schemaId={mode === 'schema' ? 'phys_dipole_rc' : null}
          drawCommands={mode === 'dessin' ? COMMANDES_DE_DESSIN : null}
          onStudentMessage={recevoirQuestion}
          assistantReply={envoyes.length ? 'τ vaut RC : c’est le temps au bout duquel la charge atteint 63 % de sa valeur finale.' : null}
          busy={busy}
          voiceEnabled
        />
      </div>
    </div>
  );
}
