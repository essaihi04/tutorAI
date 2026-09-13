import assert from 'node:assert/strict';
import { mkdtemp, writeFile, unlink, rmdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { build } from 'esbuild';

const frontend = fileURLToPath(new URL('..', import.meta.url));
const directory = await mkdtemp(path.join(tmpdir(), 'moalim-render-tests-'));
const output = path.join(directory, 'render.cjs');
try {
  const result = await build({
    stdin: {
      contents: `
        export { renderMindMapLabel as renderMap } from './src/components/session/MindMap';
        export { renderMixedLatexToHtml as renderText } from './src/components/exam/LatexRenderer';
      `,
      resolveDir: frontend,
      loader: 'tsx',
    },
    bundle: true, platform: 'node', format: 'cjs', write: false,
    jsx: 'automatic', loader: { '.css': 'empty' }, logLevel: 'silent',
  });
  await writeFile(output, result.outputFiles[0].contents);
  const { renderMap, renderText } = createRequire(import.meta.url)(output);
  for (const label of ['<b>raw HTML</b>', '<svg/onload=alert()>', '</div><img src=x>']) {
    const html = renderMap(label);
    assert.ok(!html.includes(label), `Mind map interpreted a label as markup: ${label}`);
    assert.ok(html.includes('&lt;'), 'Mind map should display escaped label text');
  }
  const table = renderText('| Name | Value |\n|---|---|\n| <img src=x onerror=alert(1)> | $x^2$ |');
  assert.ok(table.includes('<table') && table.includes('katex'));
  assert.ok(!table.includes('<img'));
  assert.ok(!renderText('$\\href{javascript:alert(1)}{click}$').includes('href="javascript:'));
  assert.ok(renderMap('$x^2$').includes('katex'));
  console.log('6 real rendering checks passed: escaped labels, safe tables/links, preserved math');
} finally {
  await unlink(output).catch(error => { if (error.code !== 'ENOENT') throw error; });
  await rmdir(directory);
}
