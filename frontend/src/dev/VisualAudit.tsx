/**
 * Planche de contrôle des visuels — page de DÉVELOPPEMENT uniquement.
 *
 * Elle rend, côte à côte et sans backend, la totalité de la bibliothèque de
 * schémas SVG et un échantillon des trois moteurs scientifiques. On y regarde
 * ce qu'un élève verrait vraiment : un schéma dont les annotations tombent
 * hors du cadre, une figure trop dense ou un moteur muet ne se voient pas dans
 * un test unitaire, et se voient tout de suite ici.
 *
 * Route : /dev/visual-audit (montée seulement quand import.meta.env.DEV).
 */
import { useMemo, useState } from 'react';
import { getAllSchemas } from '../components/session/schemas';
import SVGSchemaViewer from '../components/session/schemas/SVGSchemaViewer';
import { SVG_DEFS } from '../components/session/schemas/svgDefs';
import ScientificVisual from '../components/session/scientific/ScientificVisual';
import type { ScientificSchema } from '../components/session/schemas/types';
import type { ScientificVisualSpec } from '../components/session/scientific/types';

interface Verdict {
  level: 'ok' | 'warn' | 'error';
  message: string;
}

/** Contrôles mécaniques : ce qu'on peut affirmer sans regarder l'écran. */
function inspect(schema: ScientificSchema): Verdict[] {
  const verdicts: Verdict[] = [];
  const [minX, minY, width, height] = schema.viewBox.split(/\s+/).map(Number);
  const box = { minX, minY, maxX: minX + width, maxY: minY + height };

  if (![minX, minY, width, height].every(Number.isFinite) || width <= 0 || height <= 0) {
    verdicts.push({ level: 'error', message: `viewBox illisible : "${schema.viewBox}"` });
  }

  const ratio = width / height;
  if (ratio < 0.9 || ratio > 2.6) {
    verdicts.push({ level: 'warn', message: `format ${ratio.toFixed(2)}:1 — inhabituel pour un cadre de cours` });
  }

  if (!schema.layers.length) verdicts.push({ level: 'error', message: 'aucun calque' });
  if (!schema.annotations.length) verdicts.push({ level: 'warn', message: 'aucune annotation cliquable' });
  if (!schema.highlights.length) verdicts.push({ level: 'warn', message: 'aucun point à surligner (le tuteur ne peut rien pointer)' });
  if (schema.keywords.length < 4) verdicts.push({ level: 'warn', message: `${schema.keywords.length} mots-clés — recherche fragile` });
  if (!schema.keywords.some(word => /[؀-ۿ]/.test(word))) {
    verdicts.push({ level: 'warn', message: 'aucun mot-clé en arabe — introuvable si l\'élève écrit en darija' });
  }

  const svg = schema.layers.map(layer => layer.svgContent).join('');
  if (!/[؀-ۿ]/.test(svg)) {
    verdicts.push({ level: 'warn', message: 'aucun texte arabe dans le dessin (le BAC est bilingue)' });
  }

  const outside = schema.annotations.filter(a =>
    a.x < box.minX - 2 || a.y < box.minY - 2 || a.x + a.width > box.maxX + 2 || a.y + a.height > box.maxY + 2);
  if (outside.length) {
    verdicts.push({ level: 'error', message: `${outside.length} annotation(s) hors cadre : ${outside.map(a => a.id).join(', ')}` });
  }

  const missingDescription = schema.annotations.filter(a => !a.description?.trim());
  if (missingDescription.length) {
    verdicts.push({ level: 'warn', message: `${missingDescription.length} annotation(s) sans explication au clic` });
  }

  const orphanHighlights = schema.highlights.filter(h => h.targetLayerId && !schema.layers.some(l => l.id === h.targetLayerId));
  if (orphanHighlights.length) {
    verdicts.push({ level: 'error', message: `surlignage vers un calque inexistant : ${orphanHighlights.map(h => h.id).join(', ')}` });
  }

  // Comparaison au TEXTE des defs, pas au DOM : au premier rendu le SVG du
  // schéma n'est pas encore monté, et tout marqueur passerait pour absent.
  // Un schéma peut apporter ses propres defs (un `clipPath` livré avec un
  // dessin importé, par exemple) : les siennes comptent autant que les
  // partagées, sinon on signale une absence qui n'existe pas.
  const declaredMarkers = new Set([
    ...Array.from(SVG_DEFS.matchAll(/id="([^"]+)"/g)).map(match => match[1]),
    ...Array.from(svg.matchAll(/id="([^"]+)"/g)).map(match => match[1]),
  ]);
  const usedMarkers = new Set(Array.from(svg.matchAll(/url\(#([^)]+)\)/g)).map(match => match[1]));
  const missingMarkers = [...usedMarkers].filter(id => !declaredMarkers.has(id));
  if (missingMarkers.length) {
    verdicts.push({ level: 'error', message: `marqueur SVG absent des defs : ${missingMarkers.join(', ')}` });
  }

  const lastDelay = Math.max(0, ...schema.layers.map(layer => layer.delay ?? 0));
  if (lastDelay > 6000) {
    verdicts.push({ level: 'warn', message: `animation complète en ${(lastDelay / 1000).toFixed(1)} s — trop longue` });
  }

  if (!verdicts.length) verdicts.push({ level: 'ok', message: 'aucun défaut mécanique' });
  return verdicts;
}

const SAMPLES: { title: string; spec: ScientificVisualSpec }[] = [
  {
    title: 'Three.js — mitochondrie manipulable',
    spec: {
      engine: 'three', model: 'mitochondrion', title: 'Mitochondrie 3D interactive',
      description: 'Double membrane, crêtes, matrice et ADN mitochondrial circulaire.',
      autoplay: true, labels: true, focus: 'all',
    },
  },
  {
    title: 'JSXGraph — bilan des forces',
    spec: {
      engine: 'jsxgraph', title: 'Bilan des forces sur un solide', boundingBox: [-5, 5, 5, -5], axis: false,
      elements: [
        { type: 'point', points: [{ x: 0, y: 0 }], label: 'S', color: 'cyan' },
        { type: 'arrow', points: [{ x: 0, y: 0 }, { x: 0, y: -3 }], label: 'P', color: 'red' },
        { type: 'arrow', points: [{ x: 0, y: 0 }, { x: 0, y: 3 }], label: 'R', color: 'green' },
      ],
    },
  },
  {
    title: 'JSXGraph — étude de fonction',
    spec: {
      engine: 'jsxgraph', title: 'f(x) = 1/x et son asymptote', boundingBox: [-6, 6, 6, -6], grid: true,
      elements: [
        { type: 'function', expression: '1/x', color: 'blue', label: 'f' },
        { type: 'line', points: [{ x: 0, y: -6 }, { x: 0, y: 6 }], dashed: true, color: 'red' },
        { type: 'point', points: [{ x: 1, y: 1 }], label: 'A(1;1)' },
      ],
    },
  },
  {
    // ── Deux axes, deux grandeurs : l'échelle se libère ──
    // Un pH contre un volume : imposer « 1 mL = 1 unité de pH » étirait le
    // cadre pour tenir l'échelle, et l'écran affichait jusqu'à pH = −15.
    // Un pH négatif n'existe pas — l'élève le lisait quand même.
    title: 'JSXGraph — titrage (axes de grandeurs différentes)',
    spec: {
      engine: 'jsxgraph', title: 'Titrage acide fort / base forte',
      boundingBox: [-2, 14, 26, -1], axis: true, grid: true,
      xLabel: 'V (mL)', yLabel: 'pH',
      elements: [
        { type: 'function', expression: '7-3*ln(abs(10-x)+0.15)/2.3', domain: [0, 9.98], color: 'cyan' },
        { type: 'function', expression: '7+3*ln(abs(x-10)+0.15)/2.3', domain: [10.02, 24], color: 'cyan', label: 'pH = f(V)' },
        { type: 'point', points: [{ x: 10, y: 7 }], label: 'E (10 mL ; pH = 7)', color: 'red' },
        { type: 'segment', points: [{ x: 10, y: 0 }, { x: 10, y: 7 }], dashed: true, color: 'orange' },
      ],
    },
  },
  {
    // ── Deux axes, la MÊME grandeur : l'échelle reste verrouillée ──
    // Le contre-cas de la figure précédente. Une portée et une hauteur sont
    // toutes deux des longueurs : libérer l'échelle aplatirait la parabole,
    // et l'élève lirait une trajectoire qui n'est pas celle du mobile.
    title: 'JSXGraph — projectile (axes de même grandeur)',
    spec: {
      engine: 'jsxgraph', title: 'Trajectoire d’un projectile', boundingBox: [-1, 8, 17, -1],
      axis: true, xLabel: 'x (m)', yLabel: 'y (m)',
      elements: [
        { type: 'function', expression: 'x-x*x/12', domain: [0, 12], color: 'orange', label: 'trajectoire' },
        { type: 'point', points: [{ x: 6, y: 3 }], label: 'sommet', color: 'red' },
        { type: 'point', points: [{ x: 12, y: 0 }], label: 'portée', color: 'cyan' },
      ],
    },
  },
  {
    title: 'Cytoscape — respiration cellulaire',
    spec: {
      engine: 'cytoscape', title: 'De la glycolyse à la chaîne respiratoire', layout: 'breadthfirst',
      nodes: [
        { id: 'glucose', label: 'Glucose (C6)' },
        { id: 'pyruvate', label: '2 Pyruvate (C3)' },
        { id: 'krebs', label: 'Cycle de Krebs', color: 'green' },
        { id: 'chaine', label: 'Chaîne respiratoire', color: 'orange' },
      ],
      edges: [
        { from: 'glucose', to: 'pyruvate', label: 'Glycolyse (+2 ATP)' },
        { from: 'pyruvate', to: 'krebs', label: 'Acétyl-CoA' },
        { from: 'krebs', to: 'chaine', label: 'NADH, FADH₂' },
      ],
    },
  },
  {
    title: 'RoughSVG — électrolyse légendée',
    spec: {
      engine: 'roughsvg',
      title: 'Électrolyse : transformation forcée',
      description: 'Le générateur impose le courant ; oxydation à l’anode positive et réduction à la cathode négative.',
      width: 800,
      height: 440,
      elements: [
        { type: 'rect', x: 190, y: 125, width: 420, height: 235, color: 'blue', fill: '#0f2744' },
        { type: 'line', points: [{ x: 300, y: 95 }, { x: 300, y: 320 }], color: 'red', strokeWidth: 4 },
        { type: 'line', points: [{ x: 500, y: 95 }, { x: 500, y: 320 }], color: 'blue', strokeWidth: 4 },
        { type: 'rect', x: 335, y: 45, width: 130, height: 55, color: 'yellow', fill: '#3f3210' },
        { type: 'text', x: 400, y: 79, text: 'Générateur', color: 'yellow', fontSize: 18 },
        { type: 'text', x: 300, y: 390, text: 'Anode (+) : oxydation', color: 'red', fontSize: 17 },
        { type: 'text', x: 500, y: 415, text: 'Cathode (−) : réduction', color: 'blue', fontSize: 17 },
        { type: 'arrow', points: [{ x: 350, y: 250 }, { x: 275, y: 250 }], color: 'orange' },
        { type: 'arrow', points: [{ x: 450, y: 285 }, { x: 525, y: 285 }], color: 'cyan' },
        { type: 'text', x: 400, y: 190, text: 'Électrolyte : cations → cathode', color: 'white', fontSize: 16 },
      ],
      legend: [
        { color: 'red', label: 'Oxydation' },
        { color: 'blue', label: 'Réduction' },
        { color: 'cyan', label: 'Migration des cations' },
      ],
    },
  },
  {
    title: 'Matter — plan incliné (angle)',
    spec: {
      engine: 'matter', title: 'Plan incliné à 30°', width: 600, height: 320, gravity: { x: 0, y: 1 },
      bodies: [
        { id: 'plan', shape: 'rectangle', x: 300, y: 250, width: 460, height: 16, angle: 0.52, isStatic: true, label: 'Plan' },
        { id: 'caisse', shape: 'rectangle', x: 170, y: 120, width: 40, height: 40, label: 'm', color: 'orange', friction: 0.05 },
      ],
    },
  },
  {
    title: 'Matter — chute et rebond',
    spec: {
      engine: 'matter', title: 'Chute verticale', width: 600, height: 320, gravity: { x: 0, y: 1 }, autoplay: true,
      bodies: [
        { id: 'sol', shape: 'rectangle', x: 300, y: 305, width: 580, height: 20, isStatic: true, label: 'Sol' },
        { id: 'balle', shape: 'circle', x: 300, y: 60, radius: 22, label: 'Balle', color: 'orange', restitution: 0.6 },
      ],
    },
  },
  ...([
    ['svt_ch1_cycle_atp', 'cycle_complet'],
    ['svt_ch1_levures_exao', 'comparaison'],
    ['svt_ch1_chimiosmose', 'cycle_complet'],
    ['svt_ch1_carte_metabolique', 'respiration'],
    ['svt_ch1_myogrammes', 'tetanus_incomplet'],
    ['svt_ch1_cycle_actomyosine', 'cycle_complet'],
    ['svt_ch1_filieres_effort', 'effort_prolonge'],
  ] as const).map(([presetId, variant]) => ({
    title: `Preset SVT — ${presetId}`,
    spec: { engine: 'preset' as const, presetId, variant, autoplay: false, step: 99 },
  })),
];

export default function VisualAudit() {
  const schemas = useMemo(() => getAllSchemas(), []);
  const [subject, setSubject] = useState<'all' | ScientificSchema['subject']>('all');
  const shown = schemas.filter(schema => subject === 'all' || schema.subject === subject);

  const counts = schemas.reduce<Record<string, number>>((acc, schema) => {
    acc[schema.subject] = (acc[schema.subject] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <h1 className="text-2xl font-bold">Planche de contrôle des visuels</h1>
      <p className="mt-1 text-sm text-slate-400">
        {schemas.length} schémas ({Object.entries(counts).map(([key, value]) => `${key} ${value}`).join(' · ')})
        — chaque vignette est rendue par le composant réel de la session.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        {(['all', 'svt', 'physics', 'chemistry', 'math'] as const).map(key => (
          <button
            key={key}
            onClick={() => setSubject(key)}
            className={`rounded-lg px-3 py-1.5 text-sm ${subject === key ? 'bg-cyan-500 text-slate-950' : 'bg-white/10'}`}
          >
            {key}
          </button>
        ))}
      </div>

      <h2 className="mt-8 text-lg font-semibold">Moteurs scientifiques</h2>
      <div className="mt-3 grid gap-4 lg:grid-cols-2">
        {SAMPLES.map(sample => (
          <section key={sample.title} className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
            <h3 className="mb-2 text-sm font-semibold text-cyan-200">{sample.title}</h3>
            <ScientificVisual spec={sample.spec} />
          </section>
        ))}
      </div>

      <h2 className="mt-10 text-lg font-semibold">Bibliothèque de schémas</h2>
      <div className="mt-3 grid gap-5 xl:grid-cols-2">
        {shown.map(schema => {
          const verdicts = inspect(schema);
          const worst = verdicts.some(v => v.level === 'error') ? 'error'
            : verdicts.some(v => v.level === 'warn') ? 'warn' : 'ok';
          return (
            <section key={schema.id} data-audit-id={schema.id} data-audit-level={worst}
              className="rounded-xl border border-white/10 bg-white/[0.03] p-3">
              <header className="mb-2 flex flex-wrap items-baseline gap-2">
                <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${
                  worst === 'error' ? 'bg-red-500/20 text-red-300'
                    : worst === 'warn' ? 'bg-amber-500/20 text-amber-200' : 'bg-emerald-500/20 text-emerald-200'}`}>
                  {worst}
                </span>
                <h3 className="text-sm font-semibold">{schema.title}</h3>
                <code className="text-[11px] text-slate-400">{schema.id}</code>
                <span className="ml-auto text-[11px] text-slate-400">
                  {schema.layers.length} calques · {schema.annotations.length} annotations · {schema.highlights.length} surlignages
                </span>
              </header>
              <ul className="mb-2 space-y-0.5 text-[11px]">
                {verdicts.map(verdict => (
                  <li key={verdict.message} className={
                    verdict.level === 'error' ? 'text-red-300' : verdict.level === 'warn' ? 'text-amber-200' : 'text-emerald-300'}>
                    • {verdict.message}
                  </li>
                ))}
              </ul>
              <div className="h-[360px] overflow-hidden rounded-lg bg-white">
                <SVGSchemaViewer schema={schema} autoAnimate={false} handDrawn />
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
