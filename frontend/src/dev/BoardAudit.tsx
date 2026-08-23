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
import type { ScientificVisualSpec } from '../components/session/scientific/types';

type Mode = 'cours' | 'schema' | 'dessin' | 'roughsvg' | 'cytoscape' | 'jsxgraph' | 'matter';

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

/* ------------------------------------------------------------------ */
/*  Les quatre moteurs, dans un tableau de COURS                       */
/*                                                                     */
/*  C'est la forme exacte qui disparaissait : un titre, une phrase, et */
/*  la ligne `scientific` qui porte la figure. Un titre et une phrase   */
/*  se rejouent très bien en direct — le tableau partait donc en script */
/*  « prof en direct », et la conversion jetait la figure en silence.   */
/*  L'élève entendait « regarde le schéma » devant un tableau vide.     */
/*                                                                     */
/*  Les spécifications ci-dessous sont celles que le SERVEUR émet : à   */
/*  la lettre ce que rendent `normalize_scientific_visual` puis         */
/*  `scientific_visual_quality` (les quatre passent à 100/100).         */
/* ------------------------------------------------------------------ */

const FIGURES: Record<string, { titre: string; phrase: string; spec: ScientificVisualSpec }> = {
  roughsvg: {
    titre: 'SVT — La mitochondrie',
    phrase: 'Sa membrane interne se replie en crêtes : la surface qui porte la chaîne respiratoire est multipliée.',
    spec: {
      engine: 'roughsvg',
      title: 'Ultrastructure de la mitochondrie',
      description: 'La membrane interne se replie en crêtes, ce qui multiplie la surface portant la chaîne respiratoire.',
      width: 760, height: 430, background: '#07111f',
      elements: [
        { type: 'ellipse', x: 380, y: 215, radiusX: 290, radiusY: 150, color: 'cyan', strokeWidth: 3 },
        { type: 'ellipse', x: 380, y: 215, radiusX: 258, radiusY: 122, color: 'green', strokeWidth: 3 },
        { type: 'polyline', color: 'green', strokeWidth: 3, points: [
          { x: 180, y: 215 }, { x: 225, y: 150 }, { x: 270, y: 215 }, { x: 315, y: 150 },
          { x: 360, y: 215 }, { x: 405, y: 150 }, { x: 450, y: 215 }, { x: 495, y: 150 }, { x: 540, y: 215 },
        ] },
        { type: 'arrow', color: 'cyan', points: [{ x: 90, y: 70 }, { x: 175, y: 160 }] },
        { type: 'arrow', color: 'green', points: [{ x: 660, y: 90 }, { x: 560, y: 165 }] },
        { type: 'arrow', color: 'orange', points: [{ x: 380, y: 400 }, { x: 380, y: 300 }] },
        { type: 'text', x: 88, y: 55, text: 'Membrane externe', color: 'cyan', fontSize: 17, align: 'start' },
        { type: 'text', x: 672, y: 75, text: 'Crêtes mitochondriales', color: 'green', fontSize: 17, align: 'end' },
        { type: 'text', x: 380, y: 420, text: 'Matrice', color: 'orange', fontSize: 17 },
      ],
      legend: [
        { color: 'cyan', label: 'Membrane externe' },
        { color: 'green', label: 'Membrane interne et crêtes' },
        { color: 'orange', label: 'Matrice' },
      ],
    },
  },
  cytoscape: {
    titre: 'SVT — La régulation de la glycémie',
    phrase: 'Le retour de la glycémie à la normale freine la sécrétion : c’est la rétroaction négative.',
    spec: {
      engine: 'cytoscape',
      title: 'Régulation de la glycémie',
      layout: 'breadthfirst',
      nodes: [
        { id: 'hyper', label: 'Hyperglycémie', color: 'red' },
        { id: 'beta', label: 'Cellules β' },
        { id: 'insuline', label: 'Insuline', color: 'green' },
        { id: 'foie', label: 'Foie : glycogénogenèse' },
        { id: 'normal', label: 'Glycémie normale', color: 'cyan' },
      ],
      edges: [
        { from: 'hyper', to: 'beta', label: 'stimule' },
        { from: 'beta', to: 'insuline', label: 'sécrète' },
        { from: 'insuline', to: 'foie', label: 'active' },
        { from: 'foie', to: 'normal', label: 'abaisse' },
        { from: 'normal', to: 'beta', label: 'rétroaction négative' },
      ],
    },
  },
  jsxgraph: {
    titre: 'Chimie — Titrage acide fort / base forte',
    phrase: 'Le saut de pH repère l’équivalence : ici V_E = 10 mL et pH_E = 7.',
    spec: {
      engine: 'jsxgraph',
      title: 'Titrage d’un acide fort par une base forte',
      boundingBox: [-2, 14, 26, -1],
      axis: true, grid: true,
      xLabel: 'V (mL)', yLabel: 'pH',
      elements: [
        { type: 'function', expression: '7-3*ln(abs(10-x)+0.15)/2.3', domain: [0, 9.98], color: 'cyan' },
        { type: 'function', expression: '7+3*ln(abs(x-10)+0.15)/2.3', domain: [10.02, 24], color: 'cyan', label: 'pH = f(V)' },
        { type: 'point', points: [{ x: 10, y: 7 }], label: 'E (10 mL ; pH = 7)', color: 'red' },
        { type: 'segment', points: [{ x: 10, y: 0 }, { x: 10, y: 7 }], dashed: true, color: 'orange' },
        { type: 'segment', points: [{ x: 0, y: 7 }, { x: 10, y: 7 }], dashed: true, color: 'orange' },
      ],
    },
  },
  matter: {
    titre: 'Physique — La chute libre',
    phrase: 'Lis la vitesse pendant la chute : elle augmente, et l’altitude diminue d’autant plus vite.',
    spec: {
      engine: 'matter',
      title: 'Chute libre : la vitesse augmente',
      width: 620, height: 400,
      gravity: { x: 0, y: 1 },
      scale: 100,
      autoplay: true,
      bodies: [
        { id: 'sol', shape: 'rectangle', x: 310, y: 380, width: 600, height: 20, isStatic: true, label: 'Sol', frictionAir: 0 },
        { id: 'bille', shape: 'circle', x: 310, y: 60, radius: 18, label: 'Bille', color: 'orange', restitution: 0.2, frictionAir: 0 },
      ],
      measures: [
        { quantity: 'time', label: 't', unit: 's', decimals: 2 },
        { quantity: 'height', body: 'bille', label: 'h', unit: 'm', decimals: 2, origin: 370 },
        { quantity: 'speed', body: 'bille', label: 'v', unit: 'm/s', decimals: 2 },
      ],
      parameters: [
        { target: 'gravity.y', label: 'Pesanteur', min: 0.2, max: 2, step: 0.1, value: 1, unit: '×g' },
      ],
    },
  },
};

/** Le tableau que le serveur enverrait : du texte, PUIS la figure. */
function tableauAvecFigure(moteur: string) {
  const figure = FIGURES[moteur];
  return {
    title: figure.titre,
    lines: [
      { type: 'title' as const, content: figure.titre },
      { type: 'text' as const, content: figure.phrase },
      { type: 'scientific' as const, content: figure.spec.title || 'Figure', scientific: figure.spec },
    ],
  };
}

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

      <p className="mt-4 text-sm text-slate-300">
        Figures générées — un tableau de cours qui PORTE la figure&nbsp;:
      </p>
      <div className="mt-2 flex flex-wrap gap-2">
        {(['roughsvg', 'cytoscape', 'jsxgraph', 'matter'] as const).map(clef => (
          <button
            key={clef}
            onClick={() => setMode(clef)}
            data-mode={clef}
            className={`rounded-lg px-3 py-1.5 text-sm ${mode === clef ? 'bg-emerald-400 text-slate-950' : 'bg-white/10'}`}
          >
            {clef} · {FIGURES[clef].titre.split('—')[0].trim()}
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
          boardContent={
            mode === 'cours' ? { title: 'Dipôle RC', lines: LIGNES_DE_COURS }
              : mode in FIGURES ? tableauAvecFigure(mode)
              : null
          }
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
