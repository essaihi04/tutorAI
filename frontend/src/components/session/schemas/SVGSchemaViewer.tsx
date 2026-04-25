import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { ScientificSchema, SchemaAnnotation } from './types';
import { SVG_DEFS } from './svgDefs';

interface SVGSchemaViewerProps {
  schema: ScientificSchema;
  activeHighlights?: string[];
  autoAnimate?: boolean;
  onAnnotationClick?: (annotation: SchemaAnnotation) => void;
  className?: string;
}

const SVGSchemaViewer: React.FC<SVGSchemaViewerProps> = ({
  schema,
  activeHighlights = [],
  autoAnimate = true,
  onAnnotationClick,
  className = '',
}) => {
  const [visibleLayers, setVisibleLayers] = useState<Set<string>>(new Set());
  const [selectedAnnotation, setSelectedAnnotation] = useState<SchemaAnnotation | null>(null);
  const [animationDone, setAnimationDone] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const timersRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  // Animate layers in sequence
  useEffect(() => {
    // Clear previous timers
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];
    setVisibleLayers(new Set());
    setAnimationDone(false);
    setSelectedAnnotation(null);

    if (!autoAnimate) {
      // Show all layers immediately
      setVisibleLayers(new Set(schema.layers.map(l => l.id)));
      setAnimationDone(true);
      return;
    }

    let maxDelay = 0;
    for (const layer of schema.layers) {
      const delay = layer.delay ?? 0;
      if (delay > maxDelay) maxDelay = delay;
      const timer = setTimeout(() => {
        setVisibleLayers(prev => new Set([...prev, layer.id]));
      }, delay);
      timersRef.current.push(timer);
    }

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
    setVisibleLayers(new Set(schema.layers.map(l => l.id)));
    setAnimationDone(true);
  }, [schema]);

  // Build SVG content
  const svgContent = schema.layers
    .filter(l => visibleLayers.has(l.id))
    .map(l => `<g class="schema-layer" data-layer-id="${l.id}" style="animation: schemaFadeIn 0.4s ease-out">${l.svgContent}</g>`)
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

  const fullSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${schema.viewBox}" 
    style="width:100%;height:100%;font-family:system-ui,sans-serif">
    <style>
      @keyframes schemaFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes schemaPulse { 0%, 100% { opacity: 0.7; transform: scale(1); } 50% { opacity: 0.3; transform: scale(1.06); } }
      .annotation-zone rect:hover { opacity: 0.22 !important; stroke-width: 2.5 !important; }
    </style>
    ${SVG_DEFS}
    ${schema.backgroundColor ? `<rect width="100%" height="100%" fill="${schema.backgroundColor}" rx="12"/>` : ''}
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
