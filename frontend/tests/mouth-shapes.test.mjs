import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { MOUTH_VISEMES, MouthShaper, bandLevels, mouthShapeWeights } from '../src/services/mouthShapes.js';

const measured = JSON.parse(readFileSync(new URL('./fixtures/mouth-shape-frames.json', import.meta.url), 'utf8'));

test('each measured word gives its own mouth shape: a, o, i, s', () => {
  for (const [expected, frames] of Object.entries(measured.frames)) {
    const mean = Object.fromEntries(MOUTH_VISEMES.map(name => [name, 0]));
    for (const levels of frames) {
      const weights = mouthShapeWeights(levels);
      for (const name of MOUTH_VISEMES) mean[name] += weights[name] / frames.length;
    }
    const best = MOUTH_VISEMES.reduce((a, b) => (mean[b] > mean[a] ? b : a));
    assert.equal(best, expected, `${expected}: ${JSON.stringify(Object.fromEntries(Object.entries(mean).map(([k, v]) => [k, +v.toFixed(2)])))}`);
  }
});

test('the weights of one instant never add up to more than one mouth', () => {
  for (const frames of Object.values(measured.frames)) {
    for (const levels of frames) {
      const total = Object.values(mouthShapeWeights(levels)).reduce((a, b) => a + b, 0);
      assert.ok(total <= 1.0001 && total >= 0, String(total));
    }
  }
  assert.equal(mouthShapeWeights(null).viseme_aa, 1, 'no measure (a laugh): wide open');
});

test('band levels average the decibels of each band', () => {
  const binHz = 48000 / 1024;
  const db = Float32Array.from({ length: 512 }, (_, i) => (i * binHz < 1000 ? -30 : -80));
  db[3] = -Infinity;
  const levels = bandLevels(db, binHz);
  assert.equal(levels.L1, -30);
  assert.ok(levels.L2 > -80 && levels.L2 < -30, 'L2 straddles 1000 Hz');
  assert.equal(levels.H, -80);
  assert.equal(levels.F, -80);
});

test('silence closes the mouth under the moustache; a syllable opens it in the shape of its sound', () => {
  const shaper = new MouthShaper();
  const a = measured.frames.viseme_aa[Math.floor(measured.frames.viseme_aa.length / 2)];
  let time = 0;
  for (let i = 0; i < 30; i++) shaper.push(a, 0, 1 / 60, (time += 1 / 60));
  assert.equal(shaper.dominant(), null);
  for (let i = 0; i < 30; i++) shaper.push(a, 1, 1 / 60, (time += 1 / 60));
  assert.ok(Object.values(shaper.weights).reduce((x, y) => x + y, 0) > 0.5);
  for (let i = 0; i < 40; i++) shaper.push(a, 0, 1 / 60, (time += 1 / 60));
  assert.equal(shaper.dominant(), null);
});

test('the shape changes smoothly and waits for the sound to come out of the speaker', () => {
  const shaper = new MouthShaper();
  const i = { L1: -40, L2: -65, H: -58, F: -90 }, s = { L1: -70, L2: -70, H: -60, F: -45 };
  assert.ok(mouthShapeWeights(i).viseme_I > 0.5 && mouthShapeWeights(s).viseme_SS > 0.9);
  let time = 0, jump = 0, previous = 0;
  for (let k = 0; k < 60; k++) {
    time += 1 / 60;
    const w = shaper.push(k < 30 ? i : s, 1, 1 / 60, time, 0.1);
    jump = Math.max(jump, Math.abs(w.viseme_SS - previous)); previous = w.viseme_SS;
    if (k === 33) assert.ok(w.viseme_SS < 0.05, 'the "s" heard 100 ms later has not shaped the mouth yet');
  }
  assert.ok(previous > 0.8, 'then the mouth takes it');
  assert.ok(jump < 0.3, `no frame jumps from one shape to another (${jump.toFixed(2)})`);
});
