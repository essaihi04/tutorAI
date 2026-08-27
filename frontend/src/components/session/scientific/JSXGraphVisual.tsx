import { useEffect, useId, useMemo, useRef, useState } from 'react';
import JXG from 'jsxgraph';
import './jsxgraph.css';
import type { JSXGraphElementSpec, JSXGraphVisualSpec, ScientificPoint } from './types';
import { compileSafeMathExpression } from './safeMathExpression';

interface JSXGraphVisualProps {
  spec: JSXGraphVisualSpec;
  /** La figure se pose SUR le tableau : ni cadre, ni fond peint. */
  transparent?: boolean;
  /**
   * Libellés d'une simulation animée. Ils sont rendus dans une couche HTML
   * fixe, distincte de la géométrie que JSXGraph redessine à chaque étape.
   */
  fixedLabels?: JSXGraphElementSpec[];
}

const BOARD_COLORS: Record<string, string> = {
  red: '#ef4444',
  blue: '#3b82f6',
  green: '#22c55e',
  orange: '#f97316',
  purple: '#a855f7',
  cyan: '#06b6d4',
  yellow: '#eab308',
  white: '#e2e8f0',
};

function resolveColor(color?: string): string {
  if (!color) return '#60a5fa';
  return BOARD_COLORS[color] || color;
}

function pointTuple(point: ScientificPoint): [number, number] {
  return [point.x, point.y];
}

function addElement(
  board: JXG.Board,
  element: JSXGraphElementSpec,
  hideLabels = false,
): JXG.GeometryElement[] {
  const created: JXG.GeometryElement[] = [];
  // Les surcharges de `board.create` exposent aussi des compositions dans
  // leur union de retour, même lorsque le type littéral crée bien un élément.
  const remember = (object: unknown): JXG.GeometryElement => {
    const geometry = object as JXG.GeometryElement;
    created.push(geometry);
    return geometry;
  };
  const color = resolveColor(element.color);
  const attributes = {
    name: hideLabels ? '' : element.label || '',
    // JSXGraph n'affiche le nom d'un segment, d'une droite, d'une flèche ou
    // d'une courbe QUE si on le demande — seul un point le montre par défaut.
    // Sans cette ligne, « P » et « R » disparaissaient d'un bilan des forces :
    // l'élève voyait deux flèches opposées sans savoir laquelle est le poids.
    withLabel: !hideLabels && Boolean(element.label),
    strokeColor: color,
    fillColor: color,
    fixed: element.draggable !== true,
    dash: element.dashed ? 2 : 0,
    strokeWidth: 2.5,
    highlightStrokeColor: color,
    highlightFillColor: color,
    label: { color: '#e2e8f0', fontSize: 14 },
  };
  const points = element.points || [];

  switch (element.type) {
    case 'point':
      if (points[0]) remember(board.create('point', pointTuple(points[0]), attributes));
      break;
    case 'segment':
      if (points.length >= 2) remember(board.create('segment', [pointTuple(points[0]), pointTuple(points[1])], attributes));
      break;
    case 'line':
      if (points.length >= 2) remember(board.create('line', [pointTuple(points[0]), pointTuple(points[1])], attributes));
      break;
    case 'arrow':
      if (points.length >= 2) remember(board.create('arrow', [pointTuple(points[0]), pointTuple(points[1])], attributes));
      break;
    case 'circle':
      if (element.center && typeof element.radius === 'number') {
        remember(board.create('circle', [pointTuple(element.center), element.radius], attributes));
      }
      break;
    case 'function':
      if (element.expression) {
        const fn = compileSafeMathExpression(element.expression);
        if (!fn) break;
        // Sans bornes, la parabole d'un projectile remonte de l'autre côté de
        // l'axe et l'élève y lit un rebond qui n'existe pas.
        remember(board.create('functiongraph', element.domain ? [fn, element.domain[0], element.domain[1]] : [fn], attributes));
      }
      break;
    case 'text':
      // Le seul moyen d'écrire une phrase SUR la figure : « Fe, le plus
      // stable » près du creux d'une courbe d'Aston vaut tout un paragraphe.
      if (!hideLabels && points[0] && element.label) {
        remember(board.create('text', [points[0].x, points[0].y, element.label], {
          ...attributes,
          fontSize: 15,
          color: '#e2e8f0',
          cssStyle: 'font-weight:600',
          anchorX: 'middle',
        }));
      }
      break;
    case 'polygon':
      if (points.length >= 3) {
        remember(board.create('polygon', points.map(pointTuple), {
          ...attributes,
          fillColor: color,
          fillOpacity: element.filled === false ? 0 : 0.18,
          borders: { strokeColor: color, strokeWidth: 2.5, highlightStrokeColor: color },
          // Les sommets d'un plan incliné ne sont pas des points de la leçon :
          // les afficher ajoute trois croix nommées A, B, C sur une figure de
          // mécanique où elles ne veulent rien dire.
          vertices: { visible: false, withLabel: false, fixed: true },
          hasInnerPoints: false,
        }));
      }
      break;
    case 'angle':
      // Première branche, sommet, seconde branche : l'ordre de lecture de la
      // notation scolaire « ASB ».
      if (points.length >= 3) {
        remember(board.create('angle', [pointTuple(points[0]), pointTuple(points[1]), pointTuple(points[2])], {
          ...attributes,
          radius: 0.8,
          fillColor: color,
          fillOpacity: 0.25,
          orthoType: 'square',
        }));
      }
      break;
    case 'area':
      // L'aire hachurée sous la courbe : c'est l'intégrale telle qu'elle est
      // définie au tableau, pas un simple tracé de plus.
      if (element.expression && element.domain) {
        const fn = compileSafeMathExpression(element.expression);
        if (!fn) break;
        const curve = remember(board.create('functiongraph', [fn, element.domain[0], element.domain[1]], {
          strokeColor: color,
          strokeWidth: 2.5,
          withLabel: false,
          fixed: true,
          highlightStrokeColor: color,
        }));
        // Les quatre poignées de l'intégrale sont faites pour être glissées.
        // Sur un tableau de cours elles se nomment A, B, C, D et l'élève les
        // lit comme des points de la leçon : quatre lettres qui n'ont aucun
        // sens à côté d'une aire.
        const hidden = { visible: false, withLabel: false, fixed: true };
        remember(board.create('integral', [element.domain, curve], {
          ...attributes,
          fillColor: color,
          fillOpacity: 0.3,
          curveLeft: hidden,
          curveRight: hidden,
          baseLeft: hidden,
          baseRight: hidden,
          // JSXGraph écrit sa propre étiquette « ∫ = 8.2500 » : une valeur
          // numérique brute, souvent fausse de sens (l'aire d'un travail est
          // en joules, pas un nombre nu) et qui chasse la légende demandée.
          withLabel: false,
          name: '',
        }));
        // On repose donc la légende du modèle au milieu de l'aire.
        if (!hideLabels && element.label) {
          const [a, b] = element.domain;
          const middle = (a + b) / 2;
          remember(board.create('text', [middle, fn(middle) / 2, element.label], {
            fontSize: 14,
            color: '#e2e8f0',
            cssStyle: 'font-weight:600',
            fixed: true,
            anchorX: 'middle',
            anchorY: 'middle',
            highlight: false,
          }));
        }
      }
      break;
  }
  return created;
}

function fixedLabelPoint(element: JSXGraphElementSpec): ScientificPoint | null {
  if (element.type === 'circle' && element.center) return element.center;
  const points = element.points || [];
  if (points.length === 1) return points[0];
  if (points.length >= 2) {
    return {
      x: (points[0].x + points[points.length - 1].x) / 2,
      y: (points[0].y + points[points.length - 1].y) / 2,
    };
  }
  return null;
}

/** L'unité écrite entre parenthèses — « t (s) » → « s ». Vide si absente. */
function unite(label?: string): string | null {
  if (typeof label !== 'string' || !label.trim()) return null;
  const trouve = label.match(/\(([^)]*)\)/);
  return (trouve ? trouve[1] : '').trim().toLowerCase();
}

/**
 * Faut-il garder une échelle identique sur les deux axes ?
 *
 * Une échelle commune est ce qui fait qu'un cercle est rond et qu'une
 * trajectoire de projectile a la forme qu'elle a vraiment. Mais elle n'a de
 * SENS que si les deux axes mesurent la même chose : dès qu'on porte un pH
 * contre un volume, imposer « un millilitre = une unité de pH » n'est pas une
 * fidélité, c'est une coïncidence.
 *
 * Constaté sur une courbe de titrage demandée entre 0 et 24 mL, pH de 0 à 14 :
 * le cadre s'étirait pour tenir l'échelle et l'écran affichait des graduations
 * jusqu'à 35 mL et jusqu'à pH = −15. Un pH négatif n'existe pas ; l'élève le
 * lisait quand même, sur une figure censée lui apprendre la lecture d'un
 * graphique.
 *
 * L'unité écrite dans `xLabel`/`yLabel` tranche, et c'est le contrat que le
 * skill impose déjà : « t (s) » contre « U (V) » sont deux grandeurs, on
 * libère ; « x (m) » contre « y (m) » sont la même, on garde. Une figure de
 * géométrie n'a pas d'axes nommés du tout — elle garde donc l'échelle, comme
 * avant.
 */
function memeEchelleSurLesDeuxAxes(xLabel?: string, yLabel?: string): boolean {
  const x = unite(xLabel);
  const y = unite(yLabel);
  if (x === null && y === null) return true;   // figure de géométrie
  return x === y;
}


/**
 * Le cadre de la figure. Sur le tableau il n'y en a pas : la figure est
 * dessinee sur l'ardoise, pas collee dessus.
 */
function CADRE_FIGURE(transparent?: boolean): string {
  return transparent
    ? 'my-0 h-full w-full p-0'
    : 'my-3 overflow-hidden rounded-xl border border-white/10 bg-slate-950/70 p-2';
}

export default function JSXGraphVisual({ spec, transparent, fixedLabels }: JSXGraphVisualProps) {
  const reactId = useId();
  const boardId = `science-board-${reactId.replace(/[^a-zA-Z0-9_-]/g, '')}`;
  const containerRef = useRef<HTMLDivElement>(null);
  const boardRef = useRef<JXG.Board | null>(null);
  const animatedObjectsRef = useRef<JXG.GeometryElement[]>([]);
  const [error, setError] = useState<string | null>(null);
  const structureKey = useMemo(() => JSON.stringify({
    boundingBox: spec.boundingBox,
    axis: spec.axis,
    grid: spec.grid,
    xLabel: spec.xLabel,
    yLabel: spec.yLabel,
    keepAspectRatio: memeEchelleSurLesDeuxAxes(spec.xLabel, spec.yLabel),
  }), [spec.axis, spec.boundingBox, spec.grid, spec.xLabel, spec.yLabel]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const structure = JSON.parse(structureKey) as {
      boundingBox?: [number, number, number, number];
      axis?: boolean;
      grid?: boolean;
      xLabel?: string;
      yLabel?: string;
      keepAspectRatio: boolean;
    };

    let board: JXG.Board | null = null;
    let observer: ResizeObserver | null = null;
    let active = true;
    const reportError = (message: string | null) => {
      queueMicrotask(() => {
        if (active) setError(message);
      });
    };
    try {
      board = JXG.JSXGraph.initBoard(boardId, {
        boundingbox: structure.boundingBox || [-5, 5, 5, -5],
        axis: structure.axis !== false,
        grid: structure.grid === true,
        defaultAxes: {
          x: {
            strokeColor: '#64748b',
            highlightStrokeColor: '#64748b',
            ticks: {
              strokeColor: '#475569',
              label: { color: '#cbd5e1' },
            },
          },
          y: {
            strokeColor: '#64748b',
            highlightStrokeColor: '#64748b',
            ticks: {
              strokeColor: '#475569',
              label: { color: '#cbd5e1' },
            },
          },
        },
        showCopyright: false,
        showNavigation: false,
        keepaspectratio: structure.keepAspectRatio,
        pan: { enabled: false },
        zoom: { wheel: false },
      });

      // Le nom et l'unité des axes font partie de la figure : au BAC, une
      // courbe dont les axes ne sont pas nommés perd des points, et l'élève
      // qui apprend sur une figure anonyme prend l'habitude de les oublier.
      const [xMin, yMax, xMax, yMin] = board.getBoundingBox();
      const axisLabel = (text: string, x: number, y: number, anchorX: 'left' | 'middle' | 'right') =>
        board!.create('text', [x, y, text], {
          fontSize: 14,
          color: '#93c5fd',
          cssStyle: 'font-weight:600',
          fixed: true,
          anchorX,
          anchorY: 'middle',
          highlight: false,
        });
      const marge = (value: number, span: number) => value - span * 0.04;
      if (structure.xLabel) axisLabel(structure.xLabel, marge(xMax, xMax - xMin), marge(0, yMax - yMin), 'right');
      if (structure.yLabel) axisLabel(structure.yLabel, marge(0, xMax - xMin), marge(yMax, yMax - yMin), 'right');
      boardRef.current = board;

      observer = new ResizeObserver(() => {
        if (!board || !container.clientWidth) return;
        board.resizeContainer(container.clientWidth, 320, true, true);
        board.fullUpdate();
      });
      observer.observe(container);
      reportError(null);
    } catch (reason) {
      console.error('[ScientificVisual][JSXGraph] Render failed:', reason);
      reportError('La figure scientifique ne peut pas être affichée.');
    }

    return () => {
      active = false;
      observer?.disconnect();
      if (board) JXG.JSXGraph.freeBoard(board);
      if (boardRef.current === board) boardRef.current = null;
      animatedObjectsRef.current = [];
    };
  }, [boardId, structureKey]);

  // La planche, ses axes et ses textes restent montés. Seuls les traits et
  // objets scientifiques sont remplacés entre deux pas d'animation.
  useEffect(() => {
    const board = boardRef.current;
    if (!board) return;
    try {
      board.suspendUpdate();
      if (animatedObjectsRef.current.length) {
        board.removeObject([...animatedObjectsRef.current].reverse());
      }
      animatedObjectsRef.current = spec.elements.flatMap(element =>
        addElement(board, element, Boolean(fixedLabels)));
      board.unsuspendUpdate();
      board.fullUpdate();
    } catch (reason) {
      board.unsuspendUpdate();
      console.error('[ScientificVisual][JSXGraph] Animation update failed:', reason);
      queueMicrotask(() => setError('La figure scientifique ne peut pas être actualisée.'));
    }
  }, [fixedLabels, spec.elements, structureKey]);

  const boundingBox = spec.boundingBox || [-5, 5, 5, -5];
  const [xMin, yMax, xMax, yMin] = boundingBox;
  const fixedText = fixedLabels?.flatMap((element, index) => {
    const point = fixedLabelPoint(element);
    if (!point || !element.label) return [];
    const left = ((point.x - xMin) / (xMax - xMin)) * 100;
    const top = ((yMax - point.y) / (yMax - yMin)) * 100;
    return [{ element, index, left, top }];
  });

  return (
    <figure className={CADRE_FIGURE(transparent)}>
      {spec.title && <figcaption className="px-2 pb-2 text-sm font-medium text-cyan-200">{spec.title}</figcaption>}
      {error && <p className="px-2 pb-2 text-sm text-red-300">{error}</p>}
      <div className="relative w-full">
        <div
          id={boardId}
          ref={containerRef}
          className="jxgbox w-full"
          style={{ height: 320, border: 0, background: 'transparent' }}
          role="img"
          aria-label={spec.title || 'Figure scientifique interactive'}
        />
        {fixedText && (
          <div className="pointer-events-none absolute inset-0" aria-hidden="true">
            {fixedText.map(({ element, index, left, top }) => (
              <span
                key={element.id || `${element.type}-${index}`}
                className="absolute max-w-[48%] -translate-x-1/2 -translate-y-1/2 text-center text-[13px] font-semibold leading-tight"
                style={{
                  left: `${left}%`,
                  top: `${top}%`,
                  color: resolveColor(element.color),
                  textShadow: '0 1px 3px rgba(2, 6, 23, 0.95)',
                }}
              >
                {element.label}
              </span>
            ))}
          </div>
        )}
      </div>
    </figure>
  );
}
