import { useEffect, useRef, useState, useCallback } from 'react';
import 'katex/dist/katex.min.css';
import katex from 'katex';

interface MindMapNode {
  id: string;
  label: string;
  level: number; // 0 = central, 1 = main branches, 2 = sub-branches, 3 = details
  color?: string;
  shape?: 'circle' | 'rectangle' | 'diamond' | 'hexagon' | 'rounded' | 'pill'; // Shape type
  icon?: string; // Emoji icon
  children?: string[]; // IDs of child nodes
  parent?: string; // ID of parent node
  description?: string; // Tooltip description
  relationType?: 'causes' | 'requires' | 'produces' | 'contains' | 'leads_to' | 'example'; // Relation type
}

interface MindMapProps {
  title: string;
  nodes: MindMapNode[];
  centerNode: string; // ID of the central concept
}

function truncateLabel(label: string, maxChars: number = 30): string {
  if (!label || label.length <= maxChars) return label;
  
  // Remove common prefixes
  const cleanLabel = label.replace(/^[-·]\s*/, '').trim();
  if (cleanLabel.length <= maxChars) return cleanLabel;
  
  // Try to truncate at word boundary
  const truncated = cleanLabel.substring(0, maxChars - 3);
  const lastSpace = truncated.lastIndexOf(' ');
  if (lastSpace > maxChars * 0.6) {
    return truncated.substring(0, lastSpace) + '...';
  }
  return truncated + '...';
}

function renderLatex(text: string): string {
  if (!text) return '';
  
  // Render inline LaTeX $...$
  const parts = text.split(/(\$[^$]+\$)/g);
  return parts.map(part => {
    if (part.startsWith('$') && part.endsWith('$')) {
      const latex = part.slice(1, -1);
      try {
        return katex.renderToString(latex, { throwOnError: false, displayMode: false });
      } catch (e) {
        return part;
      }
    }
    return part;
  }).join('');
}

// Diverse color palette for branches
const BRANCH_COLORS = [
  { main: '#3b82f6', light: '#93c5fd', dark: '#1d4ed8' }, // Blue
  { main: '#10b981', light: '#6ee7b7', dark: '#047857' }, // Green
  { main: '#f59e0b', light: '#fcd34d', dark: '#b45309' }, // Amber
  { main: '#8b5cf6', light: '#c4b5fd', dark: '#6d28d9' }, // Purple
  { main: '#ef4444', light: '#fca5a5', dark: '#b91c1c' }, // Red
  { main: '#06b6d4', light: '#67e8f9', dark: '#0e7490' }, // Cyan
];

const LEVEL_COLORS = {
  0: '#60a5fa', // Central node - blue
  1: '#4ade80', // Main branches - green
  2: '#f472b6', // Sub-branches - pink
  3: '#facc15', // Tertiary - yellow
};

// Relation type labels and styles
const RELATION_STYLES: Record<string, { label: string; color: string; dashArray?: string }> = {
  causes: { label: '→ cause', color: '#ef4444' },
  requires: { label: '← nécessite', color: '#f59e0b', dashArray: '5,3' },
  produces: { label: '→ produit', color: '#10b981' },
  contains: { label: '⊃ contient', color: '#8b5cf6', dashArray: '3,2' },
  leads_to: { label: '→ mène à', color: '#3b82f6' },
  example: { label: '≈ exemple', color: '#06b6d4', dashArray: '8,4' },
};

export default function MindMap({ title, nodes, centerNode }: MindMapProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 900, height: 650 });
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [animationPhase, setAnimationPhase] = useState(0);

  // Animation effect - reveal nodes progressively
  useEffect(() => {
    const totalNodes = nodes.length;
    if (animationPhase < totalNodes) {
      const timer = setTimeout(() => setAnimationPhase(prev => prev + 1), 150);
      return () => clearTimeout(timer);
    }
  }, [animationPhase, nodes.length]);

  useEffect(() => {
    setAnimationPhase(0); // Reset animation when nodes change
  }, [nodes]);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Auto-resize based on container
    const updateSize = () => {
      const container = containerRef.current;
      if (container) {
        setDimensions({
          width: Math.min(container.clientWidth, 1000),
          height: Math.min(600, Math.max(450, container.clientHeight)),
        });
      }
    };
    
    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  // Mouse handlers for pan
  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.button === 0) {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  }, [pan]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (isDragging) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  }, [isDragging, dragStart]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  // Zoom handler
  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(prev => Math.max(0.5, Math.min(2, prev * delta)));
  }, []);

  // Build node map
  const nodeMap = new Map<string, MindMapNode>();
  nodes.forEach(node => nodeMap.set(node.id, node));

  // Calculate positions using radial layout with 3 branches max
  const centerX = dimensions.width / 2;
  const centerY = dimensions.height / 2;
  
  interface NodePosition {
    x: number;
    y: number;
    node: MindMapNode;
    branchIndex: number; // Which main branch this belongs to
  }
  
  const positions = new Map<string, NodePosition>();
  
  // Position central node
  const center = nodeMap.get(centerNode);
  if (center) {
    positions.set(centerNode, { x: centerX, y: centerY, node: center, branchIndex: -1 });
  }

  // Position level 1 nodes (main branches) - max 3 branches spread nicely
  const level1Nodes = nodes.filter(n => n.level === 1);
  const branchCount = Math.min(level1Nodes.length, 6); // Max 6 main branches
  const angleStep = (2 * Math.PI) / Math.max(branchCount, 1);
  const radius1 = Math.min(dimensions.width, dimensions.height) * 0.28;
  
  level1Nodes.forEach((node, i) => {
    const angle = i * angleStep - Math.PI / 2; // Start from top
    const x = centerX + radius1 * Math.cos(angle);
    const y = centerY + radius1 * Math.sin(angle);
    positions.set(node.id, { x, y, node, branchIndex: i });
  });

  // Position level 2 nodes around their parents
  const level2Nodes = nodes.filter(n => n.level === 2);
  level2Nodes.forEach(node => {
    if (!node.parent) return;
    const parentPos = positions.get(node.parent);
    if (!parentPos) return;
    
    const siblings = nodes.filter(n => n.parent === node.parent && n.level === 2);
    const siblingIndex = siblings.findIndex(n => n.id === node.id);
    const siblingCount = siblings.length;
    
    const spreadAngle = Math.PI / 2.5; // 72 degrees spread
    const baseAngle = Math.atan2(parentPos.y - centerY, parentPos.x - centerX);
    const offsetAngle = siblingCount > 1 
      ? (siblingIndex - (siblingCount - 1) / 2) * (spreadAngle / (siblingCount - 1))
      : 0;
    const angle = baseAngle + offsetAngle;
    
    const radius = 90;
    const x = parentPos.x + radius * Math.cos(angle);
    const y = parentPos.y + radius * Math.sin(angle);
    
    positions.set(node.id, { x, y, node, branchIndex: parentPos.branchIndex });
  });

  // Position level 3 nodes (details)
  const level3Nodes = nodes.filter(n => n.level >= 3);
  level3Nodes.forEach(node => {
    if (!node.parent) return;
    const parentPos = positions.get(node.parent);
    if (!parentPos) return;
    
    const siblings = nodes.filter(n => n.parent === node.parent && n.level >= 3);
    const siblingIndex = siblings.findIndex(n => n.id === node.id);
    const siblingCount = siblings.length;
    
    const spreadAngle = Math.PI / 3;
    const baseAngle = Math.atan2(parentPos.y - centerY, parentPos.x - centerX);
    const offsetAngle = siblingCount > 1 
      ? (siblingIndex - (siblingCount - 1) / 2) * (spreadAngle / (siblingCount - 1))
      : 0;
    const angle = baseAngle + offsetAngle;
    
    const radius = 70;
    const x = parentPos.x + radius * Math.cos(angle);
    const y = parentPos.y + radius * Math.sin(angle);
    
    positions.set(node.id, { x, y, node, branchIndex: parentPos.branchIndex });
  });

  // Get shape for a node based on level or explicit shape
  const getNodeShape = (node: MindMapNode, level: number): string => {
    if (node.shape) return node.shape;
    // Default shapes by level
    switch (level) {
      case 0: return 'circle';      // Central = circle
      case 1: return 'rounded';     // Main branches = rounded rectangle
      case 2: return 'diamond';     // Sub-branches = diamond
      default: return 'pill';       // Details = pill
    }
  };

  // Get dimensions for different shapes
  const getShapeDimensions = (level: number) => {
    switch (level) {
      case 0: return { w: 120, h: 60, r: 60 };
      case 1: return { w: 110, h: 45, r: 12 };
      case 2: return { w: 90, h: 40, r: 8 };
      default: return { w: 80, h: 32, r: 16 };
    }
  };

  // Render different shapes
  const renderShape = (
    shape: string, 
    x: number, 
    y: number, 
    dims: { w: number; h: number; r: number },
    color: string,
    isHovered: boolean,
    isSelected: boolean,
    branchIndex: number
  ) => {
    const branchColor = BRANCH_COLORS[branchIndex % BRANCH_COLORS.length] || BRANCH_COLORS[0];
    const fillColor = branchIndex === -1 ? color : branchColor.main;
    
    const baseStyle = {
      filter: isHovered || isSelected ? 'url(#glow-strong)' : 'url(#glow)',
      transition: 'all 0.3s ease',
      transform: isHovered ? 'scale(1.08)' : 'scale(1)',
      transformOrigin: `${x}px ${y}px`,
    };

    switch (shape) {
      case 'circle':
        return (
          <circle
            cx={x}
            cy={y}
            r={dims.r}
            fill={`url(#grad-center)`}
            stroke={fillColor}
            strokeWidth={isSelected ? 4 : 2.5}
            style={baseStyle}
          />
        );
      
      case 'rectangle':
        return (
          <rect
            x={x - dims.w / 2}
            y={y - dims.h / 2}
            width={dims.w}
            height={dims.h}
            rx={4}
            fill={`url(#grad-${branchIndex})`}
            stroke={fillColor}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'rounded':
        return (
          <rect
            x={x - dims.w / 2}
            y={y - dims.h / 2}
            width={dims.w}
            height={dims.h}
            rx={dims.r}
            fill={`url(#grad-${branchIndex})`}
            stroke={fillColor}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'diamond':
        const dPoints = [
          `${x},${y - dims.h / 2}`,
          `${x + dims.w / 2},${y}`,
          `${x},${y + dims.h / 2}`,
          `${x - dims.w / 2},${y}`,
        ].join(' ');
        return (
          <polygon
            points={dPoints}
            fill={`url(#grad-${branchIndex})`}
            stroke={fillColor}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'hexagon':
        const hh = dims.h / 2;
        const hw = dims.w / 2;
        const hPoints = [
          `${x - hw * 0.5},${y - hh}`,
          `${x + hw * 0.5},${y - hh}`,
          `${x + hw},${y}`,
          `${x + hw * 0.5},${y + hh}`,
          `${x - hw * 0.5},${y + hh}`,
          `${x - hw},${y}`,
        ].join(' ');
        return (
          <polygon
            points={hPoints}
            fill={`url(#grad-${branchIndex})`}
            stroke={fillColor}
            strokeWidth={isSelected ? 3 : 2}
            style={baseStyle}
          />
        );
      
      case 'pill':
      default:
        return (
          <rect
            x={x - dims.w / 2}
            y={y - dims.h / 2}
            width={dims.w}
            height={dims.h}
            rx={dims.h / 2}
            fill={`url(#grad-${branchIndex})`}
            stroke={fillColor}
            strokeWidth={isSelected ? 3 : 1.5}
            style={baseStyle}
          />
        );
    }
  };

  // Get relation style for edge
  const getRelationStyle = (node: MindMapNode) => {
    if (node.relationType && RELATION_STYLES[node.relationType]) {
      return RELATION_STYLES[node.relationType];
    }
    return null;
  };

  return (
    <div 
      ref={containerRef}
      className="w-full h-full flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-xl overflow-hidden"
    >
      {/* Title bar with controls */}
      <div className="px-4 py-3 bg-slate-800/50 border-b border-slate-700 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <span className="text-2xl">🧠</span>
          <span>{title}</span>
        </h3>
        
        {/* Zoom controls */}
        <div className="flex items-center gap-2">
          <button 
            onClick={() => setZoom(prev => Math.max(0.5, prev - 0.1))}
            className="w-7 h-7 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm flex items-center justify-center transition-colors"
          >
            −
          </button>
          <span className="text-xs text-slate-400 w-12 text-center">{Math.round(zoom * 100)}%</span>
          <button 
            onClick={() => setZoom(prev => Math.min(2, prev + 0.1))}
            className="w-7 h-7 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm flex items-center justify-center transition-colors"
          >
            +
          </button>
          <button 
            onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }); }}
            className="ml-2 px-2 py-1 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-xs transition-colors"
          >
            Reset
          </button>
        </div>
      </div>

      {/* SVG Mind Map with pan/zoom */}
      <div 
        className="flex-1 overflow-hidden p-2 cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <svg
          ref={svgRef}
          width={dimensions.width}
          height={dimensions.height}
          className="mx-auto"
          style={{ 
            minHeight: '400px',
            transform: `scale(${zoom}) translate(${pan.x / zoom}px, ${pan.y / zoom}px)`,
            transformOrigin: 'center center',
            transition: isDragging ? 'none' : 'transform 0.1s ease-out',
          }}
        >
          {/* Gradient definitions */}
          <defs>
            {/* Center gradient */}
            <radialGradient id="grad-center">
              <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.95" />
              <stop offset="70%" stopColor="#3b82f6" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#1d4ed8" stopOpacity="0.7" />
            </radialGradient>
            
            {/* Branch gradients */}
            {BRANCH_COLORS.map((colors, i) => (
              <linearGradient key={`grad-${i}`} id={`grad-${i}`} x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={colors.light} stopOpacity="0.9" />
                <stop offset="50%" stopColor={colors.main} stopOpacity="0.85" />
                <stop offset="100%" stopColor={colors.dark} stopOpacity="0.75" />
              </linearGradient>
            ))}
            
            {/* Glow filters */}
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            <filter id="glow-strong">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            
            {/* Arrow markers for relations */}
            <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="rgba(255,255,255,0.6)" />
            </marker>
            <marker id="arrow-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#ef4444" />
            </marker>
            <marker id="arrow-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#10b981" />
            </marker>
          </defs>

          {/* Draw connections with curved paths */}
          {Array.from(positions.values()).map(({ x, y, node, branchIndex }, index) => {
            if (!node.parent || index >= animationPhase) return null;
            const parentPos = positions.get(node.parent);
            if (!parentPos) return null;
            
            const branchColor = BRANCH_COLORS[branchIndex % BRANCH_COLORS.length] || BRANCH_COLORS[0];
            const relationStyle = getRelationStyle(node);
            const strokeColor = relationStyle?.color || branchColor.main;
            const dashArray = relationStyle?.dashArray || undefined;
            
            // Calculate control point for curved path
            const midX = (parentPos.x + x) / 2;
            const midY = (parentPos.y + y) / 2;
            const dx = x - parentPos.x;
            const dy = y - parentPos.y;
            const perpX = -dy * 0.15;
            const perpY = dx * 0.15;
            
            const isHighlighted = hoveredNode === node.id || hoveredNode === node.parent;
            
            return (
              <g key={`edge-${node.id}`} className="transition-opacity duration-300">
                {/* Curved connection path */}
                <path
                  d={`M ${parentPos.x} ${parentPos.y} Q ${midX + perpX} ${midY + perpY} ${x} ${y}`}
                  stroke={strokeColor}
                  strokeWidth={isHighlighted ? 3 : 2}
                  strokeDasharray={dashArray}
                  fill="none"
                  opacity={isHighlighted ? 0.9 : 0.5}
                  markerEnd={relationStyle ? 'url(#arrow)' : undefined}
                  className="transition-all duration-300"
                  style={{
                    animation: `drawLine 0.5s ease-out ${index * 0.1}s both`,
                  }}
                />
                
                {/* Relation label */}
                {relationStyle && (
                  <text
                    x={midX + perpX}
                    y={midY + perpY - 8}
                    fill={strokeColor}
                    fontSize="9"
                    textAnchor="middle"
                    opacity={isHighlighted ? 1 : 0.6}
                    fontFamily="'Patrick Hand', cursive"
                  >
                    {relationStyle.label}
                  </text>
                )}
              </g>
            );
          })}

          {/* Draw nodes with diverse shapes */}
          {Array.from(positions.values()).map(({ x, y, node, branchIndex }, index) => {
            if (index >= animationPhase) return null;
            
            const shape = getNodeShape(node, node.level);
            const dims = getShapeDimensions(node.level);
            const color = node.color || LEVEL_COLORS[node.level as keyof typeof LEVEL_COLORS] || '#94a3b8';
            const isHovered = hoveredNode === node.id;
            const isSelected = selectedNode === node.id;
            const fontSize = node.level === 0 ? 14 : node.level === 1 ? 12 : 10;
            
            return (
              <g
                key={node.id}
                className="cursor-pointer"
                onMouseEnter={() => setHoveredNode(node.id)}
                onMouseLeave={() => setHoveredNode(null)}
                onClick={() => setSelectedNode(selectedNode === node.id ? null : node.id)}
                style={{
                  animation: `nodeAppear 0.4s ease-out ${index * 0.12}s both`,
                }}
              >
                {/* Shape */}
                {renderShape(shape, x, y, dims, color, isHovered, isSelected, branchIndex)}
                
                {/* Icon if present */}
                {node.icon && (
                  <text
                    x={x}
                    y={y - dims.h / 2 + 12}
                    fontSize="14"
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    {node.icon}
                  </text>
                )}
                
                {/* Node label */}
                <foreignObject
                  x={x - dims.w / 2 + 4}
                  y={y - dims.h / 2 + (node.icon ? 8 : 2)}
                  width={dims.w - 8}
                  height={dims.h - (node.icon ? 12 : 4)}
                  style={{ pointerEvents: 'none' }}
                >
                  <div
                    className="flex items-center justify-center h-full text-center overflow-hidden"
                    style={{
                      fontSize: `${fontSize}px`,
                      fontFamily: "'Patrick Hand', cursive",
                      color: '#ffffff',
                      fontWeight: node.level === 0 ? 'bold' : '600',
                      lineHeight: '1.15',
                      textShadow: '0 1px 2px rgba(0,0,0,0.5)',
                      wordWrap: 'break-word',
                      overflowWrap: 'break-word',
                      hyphens: 'auto',
                    }}
                  >
                    <div 
                      className="w-full"
                      style={{
                        display: '-webkit-box',
                        WebkitLineClamp: node.level === 0 ? 2 : 3,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                      }}
                      dangerouslySetInnerHTML={{ __html: renderLatex(truncateLabel(node.label, node.level === 0 ? 25 : 20)) }} 
                    />
                  </div>
                </foreignObject>
                
                {/* Tooltip on hover */}
                {isHovered && node.description && (
                  <foreignObject
                    x={x - 80}
                    y={y + dims.h / 2 + 8}
                    width={160}
                    height={60}
                  >
                    <div className="bg-slate-900/95 border border-slate-600 rounded-lg px-2 py-1.5 text-xs text-slate-200 text-center shadow-xl">
                      {node.description}
                    </div>
                  </foreignObject>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* Interactive legend */}
      <div className="px-4 py-2 bg-slate-800/50 border-t border-slate-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <div className="w-4 h-4 rounded-full bg-blue-500" />
              <span>Central</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-4 h-3 rounded bg-green-500" />
              <span>Branches</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rotate-45 bg-pink-500" />
              <span>Sous-branches</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-4 h-2.5 rounded-full bg-amber-500" />
              <span>Détails</span>
            </div>
          </div>
          
          {/* Selected node info */}
          {selectedNode && (
            <div className="text-xs text-cyan-400 flex items-center gap-2">
              <span>📌</span>
              <span>{nodeMap.get(selectedNode)?.label}</span>
              <button 
                onClick={() => setSelectedNode(null)}
                className="text-slate-500 hover:text-white"
              >
                ✕
              </button>
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes nodeAppear {
          from {
            opacity: 0;
            transform: scale(0.5);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
        @keyframes drawLine {
          from {
            stroke-dashoffset: 200;
            stroke-dasharray: 200;
          }
          to {
            stroke-dashoffset: 0;
          }
        }
      `}</style>
    </div>
  );
}
