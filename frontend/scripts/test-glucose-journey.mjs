import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';

const source = readFileSync(new URL('../src/components/session/scientific/glucoseJourneyModel.ts', import.meta.url), 'utf8');
const { outputText } = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 } });
const { GLUCOSE_STOPS: stops, glucoseStop, glucoseStopStep } = await import(`data:text/javascript;base64,${Buffer.from(outputText).toString('base64')}`);
assert.equal(stops.length, 5);
for (const stop of stops) assert.equal(stop.carbon + stop.co2, 6);
assert.deepEqual(stops.map(stop => stop.atp), [2, 2, 4, 38, 38]);
for (const max of [10, 21]) {
  for (let index = 0; index < 5; index++) assert.equal(glucoseStop(glucoseStopStep(index, max), max), index);
  assert.equal(glucoseStop(-5, max), 0);
  assert.equal(glucoseStop(NaN, max), 0);
  assert.equal(glucoseStop(999, max), 4);
}
assert.equal((38 * 30.5 / 2860 * 100).toFixed(1), '40.5');
assert.equal((2 * 30.5 / 2860 * 100).toFixed(2), '2.13');
const manifest = JSON.parse(readFileSync(new URL('../../backend/data/courses/svt_ch1_energy_course_v1.json', import.meta.url), 'utf8'));
const slide = manifest.activities.flatMap(activity => activity.slides).find(slide => slide.id === 'energy_a08_s02');
assert.equal(slide.visual.scientific.presetId, 'svt_ch1_schema_bilan_annote');
assert.equal(slide.screen_content.bullets.length, 0);
console.log('Glucose journey: five stops, six conserved carbons, ATP yields and authored slide verified.');
