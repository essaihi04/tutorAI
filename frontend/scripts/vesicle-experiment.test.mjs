import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import ts from 'typescript';

// Tester le même modèle pur que la scène, sans navigateur ni dépendance de test ajoutée.
const path = new URL('../src/components/session/scientific/vesicleExperimentModel.ts', import.meta.url);
const compiled = ts.transpileModule(await readFile(path, 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 },
}).outputText;
const { initialVesicleState, vesicleReducer, vesicleResult, clampPH, VESICLE_CASES } = await import(`data:text/javascript;base64,${Buffer.from(compiled).toString('base64')}`);
const spec = { engine: 'preset', presetId: 'svt_ch1_vesicules_atp_synthase', variant: 'scene', step: 0 };

test('la préparation se termine dans un seul montage, sans défiler les variantes', () => {
  let state = initialVesicleState({ ...spec, autoplay: true });
  for (let i = 0; i < 4; i++) state = vesicleReducer(state, { type: 'tick' });
  assert.equal(state.step, 4);
  state = vesicleReducer(state, { type: 'finish' });
  assert.equal(state.step, 4);
  assert.equal(state.status, 'finished');
});

for (const example of VESICLE_CASES) test(`variante ${example.id} et résultat calculé`, () => {
  const state = vesicleReducer(initialVesicleState(spec), { type: 'variant', variant: example.id });
  assert.deepEqual([state.pHi, state.pHe], [example.pHi, example.pHe]);
  assert.equal(vesicleResult(state).atpSynthesis, example.id === 'acide_interne');
  assert.equal(vesicleResult(state).direction, example.id === 'equilibre' ? 'none' : example.id === 'acide_interne' ? 'outward' : 'inward');
});

test('tous les pH personnalisés utilisent la relation logarithmique', () => {
  for (let pHi = 4; pHi <= 10; pHi += .5) for (let pHe = 4; pHe <= 10; pHe += .5) {
    const result = vesicleResult({ pHi, pHe });
    assert.equal(result.atpSynthesis, pHi < pHe);
    assert.equal(result.concentrationRatio, 10 ** (pHe - pHi));
  }
});

test('modification partielle, pause, reprise, reset et préparation', () => {
  let state = initialVesicleState({ ...spec, step: 8 });
  state = vesicleReducer(state, { type: 'parameters', parameters: { pHe: 4.5 } });
  assert.equal(state.pHi, 6);
  assert.equal(vesicleResult(state).atpSynthesis, false);
  state = vesicleReducer(state, { type: 'pause' });
  assert.equal(state.status, 'idle');
  state = vesicleReducer(state, { type: 'start' });
  assert.equal(state.pHe, 4.5);
  state = vesicleReducer(state, { type: 'reset' });
  assert.deepEqual([state.pHi, state.pHe, state.step], [7, 7, 5]);
  state = vesicleReducer(state, { type: 'preparation' });
  assert.equal(state.step, 0);
});

test('le tuteur peut ouvrir, régler et figer le même montage', () => {
  let state = initialVesicleState(spec);
  state = vesicleReducer(state, { type: 'control', control: { presetId: spec.presetId, sequence: 1, command: 'set_parameters', parameters: { pHi: 5.5, pHe: 8 } } });
  assert.equal(state.step, 4);
  assert.deepEqual([state.pHi, state.pHe], [5.5, 8]);
  state = vesicleReducer(state, { type: 'control', control: { presetId: spec.presetId, sequence: 2, command: 'highlight', parameters: { variant: 'equilibre' } } });
  assert.equal(state.status, 'idle');
  assert.deepEqual([state.pHi, state.pHe], [7, 7]);
});

test('progression sans doublons et bornes défensives', () => {
  let state = initialVesicleState(spec);
  for (const example of [...VESICLE_CASES, VESICLE_CASES[0]]) {
    state = vesicleReducer(state, { type: 'variant', variant: example.id });
    state = vesicleReducer(state, { type: 'finish' });
  }
  assert.equal(state.completed.length, 3);
  assert.equal(clampPH(Infinity), 7);
  assert.equal(clampPH(-99), 4);
  assert.equal(clampPH(999), 10);
  assert.equal(clampPH(6.26), 6.5);
});

test('ouverture directe personnalisée et compatibilité des étapes 4–8', () => {
  assert.equal(initialVesicleState({ ...spec, variant: 'personnalisee' }).step, 5);
  assert.equal(initialVesicleState({ ...spec, parameters: { pHi: 5 } }).pHi, 5);
  for (let step = 4; step <= 8; step++) assert.equal(initialVesicleState({ ...spec, step }).step, step);
  const custom = vesicleReducer(initialVesicleState(spec), { type: 'variant', variant: 'personnalisee' });
  assert.equal(custom.step, 4);
  const highlighted = vesicleReducer(initialVesicleState(spec), { type: 'control', control: { sequence: 1, presetId: spec.presetId, command: 'highlight', parameters: { variant: 'scene' } } });
  assert.equal(highlighted.step, 8);
});
