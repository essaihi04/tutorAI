import { memo } from 'react';
import 'katex/dist/katex.min.css';
import katex from 'katex';

/**
 * Render a mixed text + LaTeX string.
 *
 * Supported delimiters:
 *   - `$...$`     → inline math
 *   - `$$...$$`   → display math
 *   - `\(...\)`   → inline math (converted to `$...$`)
 *   - `\[...\]`   → display math (converted to `$$...$$`)
 *
 * Non-math segments are HTML-escaped and newlines preserved.
 * Falls back to the raw text inside `<code>` if KaTeX fails.
 */

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderLatex(latex: string, displayMode: boolean): string {
  try {
    return katex.renderToString(latex, {
      throwOnError: false,
      displayMode,
      strict: 'ignore',
      trust: false,
      output: 'html',
    });
  } catch {
    return `<code class="text-amber-700 bg-amber-50 px-1 rounded">${escapeHtml(latex)}</code>`;
  }
}

/** Convert `\(...\)` / `\[...\]` to `$...$` / `$$...$$` for uniform splitting. */
function normalizeDelimiters(text: string): string {
  return text
    .replace(/\\\[([\s\S]+?)\\\]/g, (_, m) => `$$${m}$$`)
    .replace(/\\\(([\s\S]+?)\\\)/g, (_, m) => `$${m}$`);
}

/** A line looks like a markdown table row: starts & ends with `|` and has ≥2 cells. */
function isTableRow(line: string): boolean {
  const t = line.trim();
  if (!t.startsWith('|') || !t.endsWith('|')) return false;
  // Count unescaped pipes → need at least 3 (so 2+ cells)
  return (t.match(/\|/g) || []).length >= 3;
}

/** A markdown separator row like `|---|---|` or `| :--: | --- |`. */
function isTableSeparator(line: string): boolean {
  return /^\s*\|[\s\-:|]+\|\s*$/.test(line);
}

/** Render a block of consecutive pipe-table lines to an HTML <table>. */
function renderMarkdownTable(lines: string[]): string {
  // Strip separator rows; first non-separator row becomes header if a separator exists
  const hasSeparator = lines.some(isTableSeparator);
  let html =
    '<table class="markdown-table w-full border-collapse border border-slate-300 text-[12.5px] my-2 rounded-md overflow-hidden">';
  let rowIdx = 0;
  lines.forEach((line) => {
    if (isTableSeparator(line)) return;
    // Split on `|`, drop the outer empty cells
    const raw = line.trim();
    const inner = raw.replace(/^\|/, '').replace(/\|$/, '');
    const cells = inner.split('|').map((c) => c.trim());
    const isHeader = hasSeparator && rowIdx === 0;
    const tag = isHeader ? 'th' : 'td';
    const cellCls = isHeader
      ? 'bg-slate-100 font-semibold text-slate-700'
      : 'text-slate-700';
    html += '<tr>';
    cells.forEach((cell) => {
      // Render LaTeX inside each cell (recursively, but without table support to
      // avoid pathological cases — cell content is always single-line)
      const inner = renderInlineMixedLatex(cell);
      html += `<${tag} class="border border-slate-200 px-2.5 py-1.5 align-middle text-center ${cellCls}">${inner}</${tag}>`;
    });
    html += '</tr>';
    rowIdx += 1;
  });
  html += '</table>';
  return html;
}

/**
 * Render a single-line snippet with LaTeX but without worrying about tables.
 * Used for table cells and other inline contexts.
 */
function renderInlineMixedLatex(text: string): string {
  if (!text) return '';
  const src = normalizeDelimiters(text);
  const parts = src.split(/(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/g);
  return parts
    .map((part) => {
      if (!part) return '';
      if (part.startsWith('$$') && part.endsWith('$$') && part.length >= 4) {
        return renderLatex(part.slice(2, -2), true);
      }
      if (part.startsWith('$') && part.endsWith('$') && part.length >= 2) {
        return renderLatex(part.slice(1, -1), false);
      }
      return escapeHtml(part);
    })
    .join('');
}

export function renderMixedLatexToHtml(text: string): string {
  if (!text) return '';
  const src = normalizeDelimiters(text);

  // ── 1. Extract markdown tables into their own blocks ──
  // We walk the text line-by-line and group consecutive table rows together.
  const lines = src.split('\n');
  const blocks: Array<{ kind: 'text' | 'table'; body: string }> = [];
  let buf: string[] = [];
  let tableBuf: string[] = [];
  const flushText = () => {
    if (buf.length) {
      blocks.push({ kind: 'text', body: buf.join('\n') });
      buf = [];
    }
  };
  const flushTable = () => {
    if (tableBuf.length) {
      // Need at least 2 rows to be a real table (header + separator, or 2 data rows)
      if (tableBuf.length >= 2) {
        blocks.push({ kind: 'table', body: tableBuf.join('\n') });
      } else {
        // Single pipe-row → treat as text
        buf.push(...tableBuf);
      }
      tableBuf = [];
    }
  };
  for (const line of lines) {
    if (isTableRow(line) || (tableBuf.length > 0 && isTableSeparator(line))) {
      // Continue or start table
      if (buf.length) flushText();
      tableBuf.push(line);
    } else {
      if (tableBuf.length) flushTable();
      buf.push(line);
    }
  }
  flushTable();
  flushText();

  // ── 2. Render each block ──
  return blocks
    .map((b) => {
      if (b.kind === 'table') {
        return renderMarkdownTable(b.body.split('\n'));
      }
      // Text block: split on $$...$$ / $...$ for KaTeX
      const parts = b.body.split(/(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/g);
      return parts
        .map((part) => {
          if (!part) return '';
          if (part.startsWith('$$') && part.endsWith('$$') && part.length >= 4) {
            return renderLatex(part.slice(2, -2), true);
          }
          if (part.startsWith('$') && part.endsWith('$') && part.length >= 2) {
            return renderLatex(part.slice(1, -1), false);
          }
          return escapeHtml(part).replace(/\n/g, '<br/>');
        })
        .join('');
    })
    .join('');
}

interface Props {
  children: string;
  className?: string;
  as?: keyof React.JSX.IntrinsicElements;
}

/**
 * Renders a string that may contain LaTeX delimiters.
 * Use `as="span"` for inline flows (e.g. inside a button label).
 */
const LatexRenderer = memo(function LatexRenderer({ children, className = '', as = 'div' }: Props) {
  const Tag = as as keyof React.JSX.IntrinsicElements;
  const html = renderMixedLatexToHtml(children || '');
  return (
    <Tag
      className={className}
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
});

export default LatexRenderer;
