import type { ScientificSchema } from './types';
import { SVG_DEFS } from './svgDefs';

import * as svtModule from './schemas_svt';
import * as physModule from './schemas_physics';
import * as chemModule from './schemas_chemistry';
import * as mathModule from './schemas_math';

// ═══════════════════════════════════════════════════════════════
// Central Schema Registry
// ═══════════════════════════════════════════════════════════════

function collectSchemas(module: Record<string, unknown>): ScientificSchema[] {
  const schemas: ScientificSchema[] = [];
  for (const key of Object.keys(module)) {
    const val = module[key];
    if (val && typeof val === 'object' && 'id' in val && 'layers' in val && 'viewBox' in val) {
      schemas.push(val as ScientificSchema);
    }
  }
  return schemas;
}

const ALL_SCHEMAS: ScientificSchema[] = [
  ...collectSchemas(svtModule),
  ...collectSchemas(physModule),
  ...collectSchemas(chemModule),
  ...collectSchemas(mathModule),
];

// Index by id for O(1) lookup
const SCHEMA_BY_ID = new Map<string, ScientificSchema>();
for (const s of ALL_SCHEMAS) {
  SCHEMA_BY_ID.set(s.id, s);
}

// ═══════════════════════════════════════════════════════════════
// Public API
// ═══════════════════════════════════════════════════════════════

/** Get a schema by its exact id */
export function getSchemaById(id: string): ScientificSchema | undefined {
  return SCHEMA_BY_ID.get(id);
}

/** Get all schemas */
export function getAllSchemas(): ScientificSchema[] {
  return ALL_SCHEMAS;
}

/** Get schemas filtered by subject */
export function getSchemasBySubject(subject: ScientificSchema['subject']): ScientificSchema[] {
  return ALL_SCHEMAS.filter(s => s.subject === subject);
}

/**
 * Search schemas by keyword(s). Returns schemas ranked by relevance score.
 * Supports French, Arabic, and technical terms.
 */
export function searchSchemas(query: string, subject?: ScientificSchema['subject']): ScientificSchema[] {
  const normalised = query.toLowerCase().trim();
  if (!normalised) return [];

  const tokens = normalised.split(/[\s,;]+/).filter(t => t.length > 1);

  const scored: { schema: ScientificSchema; score: number }[] = [];

  for (const schema of ALL_SCHEMAS) {
    if (subject && schema.subject !== subject) continue;

    let score = 0;

    // Exact id match — highest priority
    if (schema.id === normalised) {
      score += 100;
    }

    // Title match
    const titleLower = schema.title.toLowerCase();
    for (const token of tokens) {
      if (titleLower.includes(token)) score += 10;
    }

    // Keyword match
    for (const kw of schema.keywords) {
      const kwLower = kw.toLowerCase();
      for (const token of tokens) {
        if (kwLower === token) score += 8;
        else if (kwLower.includes(token) || token.includes(kwLower)) score += 4;
      }
    }

    // Category match
    for (const token of tokens) {
      if (schema.category.includes(token)) score += 2;
    }

    if (score > 0) {
      scored.push({ schema, score });
    }
  }

  scored.sort((a, b) => b.score - a.score);
  return scored.map(s => s.schema);
}

/**
 * Find the single best schema matching a query string.
 * Returns undefined if no match found.
 */
export function findBestSchema(query: string, subject?: ScientificSchema['subject']): ScientificSchema | undefined {
  const results = searchSchemas(query, subject);
  return results.length > 0 ? results[0] : undefined;
}

// Re-export types and defs
export type { ScientificSchema, SchemaLayer, SchemaAnnotation, SchemaHighlight } from './types';
export { SVG_DEFS };
