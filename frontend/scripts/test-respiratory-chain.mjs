import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import ts from 'typescript';

const source = readFileSync(new URL('../src/components/session/scientific/respiratoryChainModel.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 } });
const { respiratoryGradientFrame: frame, RESPIRATORY_YIELDS: yields, RESPIRATORY_MAX_STEP: max } =
  await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);

assert.equal(yields.nadh.atp, 3);
assert.equal(yields.fadh2.atp, 2);
assert.equal(max, 18);
const frames = Array.from({ length: max + 1 }, (_, step) => frame(step));
for (const current of frames) {
  assert.equal(current.intermembraneParticles + current.matrixParticles, 22);
  assert.equal(current.intermembraneConcentration + current.matrixConcentration, 110);
  assert.ok(current.matrixPH >= current.intermembranePH);
  assert.ok(Math.abs(current.concentrationRatio - 10 ** current.deltaPH) < 1e-10);
}
assert.equal(frames[7].intermembraneParticles, 20);
assert.equal(frames[7].matrixParticles, 2);
assert.equal(frames[7].intermembranePH, 7);
assert.equal(frames[7].matrixPH, 8);
assert.equal(frames[11].pumping, true);
assert.equal(frames[11].makingAtp, true);
for (let step = 14; step <= max; step++) {
  assert.ok(frames[step].deltaPH < frames[step - 1].deltaPH);
  assert.ok(frames[step].intermembraneParticles <= frames[step - 1].intermembraneParticles);
  assert.ok(frames[step].matrixParticles >= frames[step - 1].matrixParticles);
  assert.equal(frames[step].pumping, false);
}
assert.equal(frames[max].deltaPH, 0);
assert.equal(frames[max].returning, false);
assert.equal(frames[max].makingAtp, false);
assert.equal(frames[max].intermembraneParticles, frames[max].matrixParticles);
assert.deepEqual(frame(-5), frame(0));
assert.deepEqual(frame(NaN), frame(0));
assert.deepEqual(frame(999), frame(max));
console.log('Respiratory-chain model: 19 frames, concentrations, pH, relaxation and school ATP yields verified.');

// Render the actual authored molecule components, including the waiting states.
const require = createRequire(import.meta.url);
const reactionSource = readFileSync(new URL('../src/components/session/scientific/RespiratoryReactions.tsx', import.meta.url), 'utf8');
const reactionModule = ts.transpileModule(reactionSource, { compilerOptions: {
  target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022, jsx: ts.JsxEmit.ReactJSX,
} }).outputText.replaceAll('"react/jsx-runtime"', JSON.stringify(pathToFileURL(require.resolve('react/jsx-runtime')).href));
const { OxygenReaction, AtpReaction, DonorReaction } = await import(`data:text/javascript;base64,${Buffer.from(reactionModule).toString('base64')}`);
const markup = (Component, props) => renderToStaticMarkup(createElement('svg', {}, createElement(Component, { ...props, onReplay() {} })));
assert.match(markup(OxygenReaction, { step: 6 }), /data-reaction-state="waiting"/);
const receiving = markup(OxygenReaction, { step: 7 });
assert.match(receiving, /data-reaction-state="receiving"/);
assert.equal((receiving.match(/>e⁻<\/text>/g) || []).length, 4);
assert.equal((receiving.match(/>H⁺<\/text>/g) || []).length, 4);
const water = markup(OxygenReaction, { step: 8 });
assert.match(water, /data-reaction-state="water"/);
assert.equal((water.match(/>H₂O<\/text>/g) || []).length, 2);
assert.doesNotMatch(water, />O₂<\/text>/);
assert.equal((markup(AtpReaction, { step: 9, active: false }).match(/>P<\/text>/g) || []).length, 2);
assert.match(markup(AtpReaction, { step: 10, active: false }), /rc-phosphate-binding/);
const atp = markup(AtpReaction, { step: 11, active: true });
assert.equal((atp.match(/>P<\/text>/g) || []).length, 3);
assert.match(atp, />ATP<\/text>/);
assert.doesNotMatch(atp, /ADP \+ Pi|→/);
for (const [variant, carrier] of Object.entries(yields)) {
  const props = { ...carrier, isNadh: variant === 'nadh' };
  assert.match(markup(DonorReaction, { ...props, step: 0 }), /data-reaction-state="reduced"/);
  assert.match(markup(DonorReaction, { ...props, step: 2 }), /data-reaction-state="oxidized"/);
}
console.log('Molecular reactions: donor release, O₂ waiting/capture, two waters, Pi binding and three ATP phosphates verified.');
