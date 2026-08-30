import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { ScientificSchema, SchemaAnnotation } from './types';
import { SVG_DEFS } from './svgDefs';

interface SVGSchemaViewerProps {
  schema: ScientificSchema;
  activeHighlights?: string[];
  autoAnimate?: boolean;
  handDrawn?: boolean;
  onAnnotationClick?: (annotation: SchemaAnnotation) => void;
  className?: string;
}

const SVGSchemaViewer: React.FC<SVGSchemaViewerProps> = ({
  schema,
  activeHighlights = [],
  autoAnimate = true,
  handDrawn = false,
  onAnnotationClick,
  className = '',
}) => {
  const [selectedAnnotation, setSelectedAnnotation] = useState<SchemaAnnotation | null>(null);
  const [animationDone, setAnimationDone] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  /**
   * ── La mise en scène est faite par CSS, plus par React ──
   *
   * Les couches apparaissaient une à une par `setState`, et le schéma entier
   * est écrit dans le DOM par `innerHTML` : à CHAQUE couche ajoutée, tout le
   * SVG était reconstruit et reparsé. Or chaque `<g>` porte une animation
   * d'entrée en ligne — recréé, il la rejoue. Un schéma de six couches
   * repartait donc six fois de zéro, et l'élève voyait un clignotement qui
   * durait exactement le temps de la mise en place.
   *
   * Les couches sont désormais TOUTES écrites d'emblée, chacune avec son
   * propre `animation-delay` : le navigateur les échelonne sans que la chaîne
   * SVG ne bouge d'un caractère. Il ne reste ici qu'une échéance, pour savoir
   * quand la mise en place est finie — elle ne touche pas au dessin.
   */
  useEffect(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setAnimationDone(!autoAnimate);
    setSelectedAnnotation(null);
    if (!autoAnimate) return;

    const maxDelay = schema.layers.reduce((max, layer) => Math.max(max, layer.delay ?? 0), 0);
    const doneTimer = setTimeout(() => setAnimationDone(true), maxDelay + 600);
    timersRef.current.push(doneTimer);

    return () => {
      timersRef.current.forEach(clearTimeout);
      timersRef.current = [];
    };
  }, [schema, autoAnimate]);

  const handleAnnotationClick = useCallback((ann: SchemaAnnotation) => {
    setSelectedAnnotation(prev => prev?.id === ann.id ? null : ann);
    onAnnotationClick?.(ann);
  }, [onAnnotationClick]);

  const skipAnimation = useCallback(() => {
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setAnimationDone(true);
  }, []);

  // Build SVG content
  //
  // Toutes les couches, tout de suite : c'est leur `animation-delay` qui les
  // échelonne. `both` les garde invisibles AVANT leur tour — sans lui, elles
  // seraient posées d'un bloc puis disparaîtraient pour se refondre.
  const svgContent = schema.layers
    .map(l => {
      const entree = animationDone
        ? 'opacity:1'
        : `animation: schemaFadeIn 0.4s ease-out ${l.delay ?? 0}ms both`;
      return `<g class="schema-layer" data-layer-id="${l.id}" style="${entree}">${l.svgContent}</g>`;
    })
    .join('\n');

  // Annotation overlays (clickable zones)
  const annotationOverlays = animationDone ? schema.annotations.map(ann => {
    const isSelected = selectedAnnotation?.id === ann.id;
    return `<g class="annotation-zone" data-ann-id="${ann.id}">
      <rect x="${ann.x}" y="${ann.y}" width="${ann.width}" height="${ann.height}" 
        rx="6" fill="${ann.color || '#3b82f6'}" opacity="${isSelected ? 0.18 : 0.06}" 
        stroke="${ann.color || '#3b82f6'}" stroke-width="${isSelected ? 2 : 1}" 
        stroke-dasharray="${isSelected ? '0' : '4,3'}" style="cursor:pointer"/>
    </g>`;
  }).join('\n') : '';

  // Highlight pulses
  const highlightOverlays = schema.highlights
    .filter(h => activeHighlights.includes(h.id))
    .map(h => `<circle cx="${h.cx}" cy="${h.cy}" r="${h.radius}" 
      fill="none" stroke="#f59e0b" stroke-width="3" opacity="0.7" 
      style="animation: schemaPulse 1.5s ease-in-out infinite"/>
    <circle cx="${h.cx}" cy="${h.cy}" r="${h.radius + 8}" 
      fill="none" stroke="#f59e0b" stroke-width="1.5" opacity="0.3" 
      style="animation: schemaPulse 1.5s ease-in-out infinite 0.3s"/>`)
    .join('\n');

  // Le filtre « craie » couvre la SURFACE DU SCHÉMA, pas la boîte de chaque
  // forme. Un filtre en `objectBoundingBox` sur un trait horizontal ou
  // vertical a une région de hauteur — ou de largeur — NULLE : la forme
  // disparaît purement et simplement. C'est ce qui effaçait, en mode craie,
  // tous les traits de rappel des légendes, les axes des diagrammes et les
  // flèches de convergence. Seules les obliques survivaient, ce qui rendait
  // le défaut difficile à voir.
  const [boxX, boxY, boxW, boxH] = schema.viewBox.split(/\s+/).map(Number);
  const handDrawnDefs = handDrawn ? `
    <filter id="schemaHandDrawn" filterUnits="userSpaceOnUse" x="${boxX - 20}" y="${boxY - 20}" width="${boxW + 40}" height="${boxH + 40}">
      <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="1" seed="23" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.15" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <pattern id="schemaNotebookGrid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#38bdf8" stroke-width="0.65" opacity="0.22"/>
    </pattern>
  ` : '';

  const fullSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${schema.viewBox}" class="${handDrawn ? 'schema-hand-drawn' : ''}"
    style="width:100%;height:100%;font-family:system-ui,sans-serif">
    <style>
      @keyframes schemaFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes schemaPulse { 0%, 100% { opacity: 0.7; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.06); } }
      .annotation-zone rect:hover { opacity: 0.22 !important; stroke-width: 2.5 !important; }
      .schema-hand-drawn .schema-layer path,
      .schema-hand-drawn .schema-layer line,
      .schema-hand-drawn .schema-layer polyline,
      .schema-hand-drawn .schema-layer polygon,
      .schema-hand-drawn .schema-layer rect,
      .schema-hand-drawn .schema-layer circle,
      .schema-hand-drawn .schema-layer ellipse {
        filter: url(#schemaHandDrawn);
        stroke-linecap: round;
        stroke-linejoin: round;
      }
      .schema-hand-drawn text {
        font-family: "Segoe Print", "Comic Sans MS", cursive !important;
        letter-spacing: 0.15px;
      }
    </style>
    ${SVG_DEFS}
    ${handDrawnDefs}
    ${schema.backgroundColor ? `<rect width="100%" height="100%" fill="${schema.backgroundColor}" rx="12"/>` : ''}
    ${handDrawn ? '<rect width="100%" height="100%" fill="url(#schemaNotebookGrid)" rx="12" pointer-events="none"/>' : ''}
    ${svgContent}
    ${annotationOverlays}
    ${highlightOverlays}
  </svg>`;

  return (
    <div ref={containerRef} className={`relative w-full h-full flex flex-col ${className}`}>
      {/* SVG Render */}
      <div
        className="flex-1 min-h-0 overflow-hidden rounded-lg"
        dangerouslySetInnerHTML={{ __html: fullSVG }}
        onClick={(e) => {
          const target = e.target as SVGElement;
          const annGroup = target.closest('[data-ann-id]');
          if (annGroup) {
            const annId = annGroup.getAttribute('data-ann-id');
            const ann = schema.annotations.find(a => a.id === annId);
            if (ann) handleAnnotationClick(ann);
          }
        }}
      />

      {/* Skip animation button */}
      {!animationDone && (
        <button
          onClick={skipAnimation}
          className="absolute top-2 right-2 px-3 py-1 bg-white/80 hover:bg-white text-xs text-gray-600 rounded-full shadow-sm border border-gray-200 transition-colors"
        >
          Afficher tout ▶▶
        </button>
      )}

      {/* Annotation tooltip */}
      {selectedAnnotation && (
        <div className="absolute bottom-2 left-2 right-2 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-gray-200 p-3 animate-in slide-in-from-bottom-2 duration-200">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ backgroundColor: selectedAnnotation.color || '#3b82f6' }}
                />
                <span className="font-semibold text-sm text-gray-900">
                  {selectedAnnotation.label}
                </span>
              </div>
              <p className="text-xs text-gray-600 mt-1 leading-relaxed">
                {selectedAnnotation.description}
              </p>
            </div>
            <button
              onClick={() => setSelectedAnnotation(null)}
              className="text-gray-400 hover:text-gray-600 text-sm flex-shrink-0"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Attribution du dessin importé — exigée par la licence CC BY, donc
          affichée avec le schéma et non reléguée dans le code. */}
      {schema.credit && (
        <div className="absolute bottom-1 right-2 text-[9px] leading-tight text-gray-400/90 max-w-[60%] text-right pointer-events-none">
          {schema.credit}
        </div>
      )}

      {/* Layer legend (small) */}
      {animationDone && schema.layers.length > 2 && (
        <div className="absolute top-2 left-2 flex flex-wrap gap-1 max-w-[60%]">
          {schema.layers.filter(l => l.label !== 'Titre' && l.label !== 'Fond').slice(0, 6).map(l => (
            <span
              key={l.id}
              className="px-2 py-0.5 bg-white/70 text-[10px] text-gray-500 rounded-full border border-gray-200"
            >
              {l.label}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};

export default SVGSchemaViewer;
