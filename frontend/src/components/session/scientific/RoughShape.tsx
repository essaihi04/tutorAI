import { useMemo } from 'react';
import rough from 'roughjs';
import type { CSSProperties } from 'react';
import type { Options } from 'roughjs/bin/core';

interface Point {
  x: number;
  y: number;
}

interface RoughShapeProps {
  kind: 'line' | 'rectangle' | 'circle' | 'linearPath' | 'polygon';
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  points?: Point[];
  stroke: string;
  strokeWidth: number;
  fill?: string;
  seed: number;
  style?: CSSProperties;
}

export default function RoughShape({
  kind, x = 0, y = 0, width = 0, height = 0, radius = 0, points = [],
  stroke, strokeWidth, fill, seed, style,
}: RoughShapeProps) {
  const paths = useMemo(() => {
    const generator = rough.generator();
    const options: Options = {
      stroke,
      strokeWidth,
      fill,
      fillStyle: 'solid',
      roughness: 0.75,
      bowing: 0.8,
      seed: Math.max(1, seed),
    };
    const tuples = points.map(point => [point.x, point.y] as [number, number]);
    switch (kind) {
      case 'line':
        return tuples.length >= 2 ? generator.toPaths(generator.line(tuples[0][0], tuples[0][1], tuples[1][0], tuples[1][1], options)) : [];
      case 'rectangle':
        return generator.toPaths(generator.rectangle(x, y, width, height, options));
      case 'circle':
        return generator.toPaths(generator.circle(x, y, radius * 2, options));
      case 'linearPath':
        return tuples.length >= 2 ? generator.toPaths(generator.linearPath(tuples, options)) : [];
      case 'polygon':
        return tuples.length >= 3 ? generator.toPaths(generator.polygon(tuples, options)) : [];
    }
  }, [fill, height, kind, points, radius, seed, stroke, strokeWidth, width, x, y]);

  return (
    <>
      {paths.map((path, index) => (
        <path
          key={`${seed}-${index}`}
          d={path.d}
          fill={path.fill || 'none'}
          stroke={path.stroke || 'none'}
          strokeWidth={path.strokeWidth}
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={100}
          style={style}
        />
      ))}
    </>
  );
}

