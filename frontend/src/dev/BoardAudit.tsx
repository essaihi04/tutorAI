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

type Mode = 'cours' | 'schema' | 'dessin' | 'roughsvg' | 'cytoscape' | 'jsxgraph' | 'matter'
  | 'echiquier' | 'qcm' | 'carte' | 'courbe' | 'bibliotheque' | 'effacer' | 'biologie';

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
  // ── Le cas qui rendait un croquis illisible ────────────────────────
  //
  // Le tuteur pose ses mots aux coordonnées qu'il a choisies, sans regarder
  // le tableau : deux légendes tombaient au même endroit — « direction de
  // propagation » écrite PAR-DESSUS « propagation » — et un mot posé près du
  // bord sortait du cadre, l'élève lisant « …cule » au lieu de « molécule ».
  //
  // Cette étape rejoue exactement cette collision, sur un tableau qui porte
  // déjà l'étape précédente. Les trois mots doivent se lire séparément, et
  // aucun ne doit toucher le bord.
  {
    title: 'Superposition — les mots se relisent avant de s’écrire',
    elements: [
      {
        id: 'sens', type: 'arrow' as const, color: 'red', strokeWidth: 3, label: 'direction de propagation',
        points: [{ x: 300, y: 260 }, { x: 460, y: 260 }],
      },
      { id: 'double', type: 'text' as const, x: 340, y: 252, text: 'propagation', color: 'white', strokeWidth: 1, fontSize: 15 },
      { id: 'hors_cadre', type: 'text' as const, x: -30, y: 40, text: 'molécule du milieu', color: 'cyan', strokeWidth: 1, fontSize: 15 },
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

/**
 * Ce que SEUL le tableau structuré savait rendre, désormais posé dans le
 * tableau en direct.
 *
 * L'échiquier est le cas qui décide : c'est l'alignement des gamètes qui fait
 * un échiquier, et le rejouer ligne à ligne le détruirait. Il se pose donc
 * d'un bloc, à son tour dans le déroulé, pendant que le reste s'écrit.
 */
const BLOCS: Record<string, { titre: string; phrase: string; line: any }> = {
  echiquier: {
    titre: 'SVT — Échiquier de croisement',
    phrase: 'Chaque case croise un gamète du père et un gamète de la mère.',
    line: {
      type: 'table',
      content: 'Échiquier de fécondation',
      headers: ['♀ \ ♂', '$A$', '$a$'],
      rows: [
        ['$A$', '$\\frac{A}{A}$ — lisse', '$\\frac{A}{a}$ — lisse'],
        ['$a$', '$\\frac{A}{a}$ — lisse', '$\\frac{a}{a}$ — ridé'],
      ],
    },
  },
  qcm: {
    titre: 'Physique — Vérification',
    phrase: 'Réponds, puis je te dis pourquoi.',
    line: {
      type: 'qcm',
      content: 'Quand le sarcomère se raccourcit, la bande A…',
      choices: ['garde la même longueur', 'se raccourcit aussi', 'disparaît'],
      correct: 0,
      explanation: 'La bande A est la longueur des filaments de myosine : elle ne change pas, ce sont les filaments qui glissent.',
    },
  },
  carte: {
    titre: 'SVT — Carte récapitulative',
    phrase: 'Voilà tout le chapitre en une image.',
    line: {
      type: 'mindmap',
      content: 'Respiration cellulaire',
      centerNode: 'Respiration',
      mindmapNodes: [
        { id: 'n1', label: 'Glycolyse', level: 1 },
        { id: 'n2', label: 'Cycle de Krebs', level: 1 },
        { id: 'n3', label: 'Chaîne respiratoire', level: 1 },
        { id: 'n4', label: 'Cytoplasme', level: 2, parent: 'n1' },
        { id: 'n5', label: 'Matrice', level: 2, parent: 'n2' },
        { id: 'n6', label: 'Crêtes', level: 2, parent: 'n3' },
      ],
    },
  },
  courbe: {
    titre: 'Chimie — Suivi temporel',
    phrase: 'La concentration diminue, de plus en plus lentement.',
    line: {
      type: 'graph',
      content: 'Concentration au cours du temps',
      xLabel: 't (min)',
      yLabel: '[A] (mol/L)',
      xRange: [0, 60],
      yRange: [0, 1],
      curves: [{ label: '[A]', fn: 'exp(-x/20)', color: 'cyan' }],
    },
  },
};

/** Un script qui pose un bloc, comme le serveur l'enverrait. */
function scriptAvecBloc(clef: string) {
  const b = BLOCS[clef];
  return {
    title: b.titre,
    steps: [
      { action: 'write' as const, line: { type: 'title', content: b.titre } },
      { action: 'write' as const, line: { type: 'text', content: b.phrase } },
      { action: 'bloc' as const, line: b.line },
    ],
  };
}

/**
 * Les cinq formes de SVT, tracées à la craie.
 *
 * Elles vivaient sur un canvas à part, en dégradés radiaux et ombres portées.
 * Ce qui compte au BAC est gardé — la double membrane et les crêtes, la
 * bicouche orientée, les brins en opposition de phase — et le vernis, non.
 */
const CROQUIS_BIOLOGIE = [
  {
    title: 'De la cellule à la mitochondrie',
    elements: [
      { id: 'c', type: 'cell' as const, x: 130, y: 130, radius: 95, color: 'cyan', strokeWidth: 3, label: 'Cellule' },
      { id: 'n', type: 'nucleus' as const, x: 110, y: 120, radius: 38, color: 'purple', strokeWidth: 2.5, label: 'Noyau' },
      { id: 'm', type: 'mitochondria' as const, x: 280, y: 60, width: 170, height: 80, color: 'orange', strokeWidth: 3, label: 'Mitochondrie' },
      { id: 'd', type: 'dna' as const, x: 300, y: 200, width: 55, height: 130, color: 'white', strokeWidth: 2.5, label: 'ADN' },
      { id: 'b', type: 'membrane' as const, x: 60, y: 320, width: 180, height: 34, color: 'orange', strokeWidth: 2, label: 'Bicouche' },
    ],
  },
];

/**
 * Effacer et redessiner — le geste de base du professeur.
 *
 * Il pose un schéma de la bibliothèque, en parle, ESSUIE la zone de dessin,
 * puis y trace autre chose. Sans cela les figures s'empileraient : l'élève
 * verrait la partie 2 par-dessus la partie 1.
 */
function scriptEffacerPuisRedessiner() {
  return {
    title: 'SVT — Du muscle au mouvement',
    steps: [
      { action: 'write' as const, line: { type: 'title', content: 'Partie 1 — La fibre' } },
      { action: 'figure' as const, schema_id: 'svt_fibre_musculaire' },
      { action: 'pause' as const, duration: 900 },
      { action: 'erase' as const, zone: 'all' as const },
      { action: 'write' as const, line: { type: 'title', content: 'Partie 2 — Le bilan' } },
      { action: 'write' as const, line: { type: 'text', content: 'La contraction consomme de l’ATP.' } },
      { action: 'figure' as const, scientific: FIGURES.cytoscape.spec },
    ],
  };
}

/** Un schéma de la BIBLIOTHÈQUE, posé dans la zone de dessin. */
function scriptAvecSchema() {
  return {
    title: 'SVT — Ultrastructure de la fibre musculaire',
    steps: [
      { action: 'write' as const, line: { type: 'title', content: 'La fibre musculaire' } },
      { action: 'write' as const, line: { type: 'text', content: 'Repère la triade : un tubule T entre deux citernes.' } },
      { action: 'figure' as const, schema_id: 'svt_fibre_musculaire' },
    ],
  };
}

/**
 * Le script que le serveur envoie : on écrit à gauche, la figure se pose à
 * droite.
 *
 * C'est le chemin réel depuis que `_board_lines_to_live_steps` convertit une
 * ligne `scientific` en pas `figure`. Le tableau statique ne reçoit plus les
 * figures — il garde ce qui se lit d'un bloc, tableaux et QCM.
 */
function scriptAvecFigure(moteur: string) {
  const figure = FIGURES[moteur];
  return {
    title: figure.titre,
    steps: [
      { action: 'write' as const, line: { type: 'title', content: figure.titre } },
      { action: 'write' as const, line: { type: 'text', content: figure.phrase } },
      { action: 'figure' as const, scientific: figure.spec, say: figure.spec.title },
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
        Figures générées — le tableau EN DIRECT : on écrit à gauche, la figure
        se pose à droite, sans cadre ni fond.
      </p>

      <p className="mt-4 text-sm text-slate-300">
        Ce que seul le tableau structuré savait rendre — désormais dans le
        tableau en direct&nbsp;:
      </p>
      <div className="mt-2 flex flex-wrap gap-2">
        {(['echiquier', 'qcm', 'carte', 'courbe', 'bibliotheque', 'effacer', 'biologie'] as const).map(clef => (
          <button
            key={clef}
            onClick={() => setMode(clef)}
            data-mode={clef}
            className={`rounded-lg px-3 py-1.5 text-sm ${mode === clef ? 'bg-amber-400 text-slate-950' : 'bg-white/10'}`}
          >
            {clef}
          </button>
        ))}
      </div>
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
          boardContent={mode === 'cours' ? { title: 'Dipôle RC', lines: LIGNES_DE_COURS } : null}
          liveScript={
            mode in FIGURES ? (scriptAvecFigure(mode) as any)
              : mode in BLOCS ? (scriptAvecBloc(mode) as any)
              : mode === 'bibliotheque' ? (scriptAvecSchema() as any)
              : mode === 'effacer' ? (scriptEffacerPuisRedessiner() as any)
              : null
          }
          schemaId={mode === 'schema' ? 'phys_dipole_rc' : null}
          drawCommands={
            mode === 'dessin' ? COMMANDES_DE_DESSIN
              : mode === 'biologie' ? (CROQUIS_BIOLOGIE as any)
              : null
          }
          onStudentMessage={recevoirQuestion}
          assistantReply={envoyes.length ? 'τ vaut RC : c’est le temps au bout duquel la charge atteint 63 % de sa valeur finale.' : null}
          busy={busy}
          voiceEnabled
        />
      </div>
    </div>
  );
}
