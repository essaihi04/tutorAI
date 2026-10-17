import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { LipSyncAnalyser } from '../src/vendor/three-ws/lip-sync-analyser.js';

class FakeAnalyser {
  context = { sampleRate: 48000 };
  fftSize = 256;
  frequencyBinCount = 128;
  level = 0;
  getByteFrequencyData(buffer) { buffer.fill(this.level); }
}
globalThis.AnalyserNode = FakeAnalyser;
test('silent audio rests; sound opens the mouth; stop returns to rest', () => {
  const node = new FakeAnalyser();
  const lips = new LipSyncAnalyser();
  lips.connect(node);
  assert.equal(lips.getAmplitude(), 0);
  assert.ok(Object.values(lips.sample()).every(value => value === 0));
  node.level = 190;
  for (let i = 0; i < 30; i++) lips.sample();
  assert.ok(lips.getAmplitude() > .5);
  assert.ok(lips.sample().viseme_aa > .3);
  node.level = 0;
  for (let i = 0; i < 40; i++) lips.sample();
  assert.ok(lips.getAmplitude() < .001);
  lips.disconnect();
  assert.equal(lips.getAmplitude(), 0);
  assert.equal(lips.sample(), null);
});
test('distributed GLB is a self-contained humanoid rig with articulated fingers and an idle clip', () => {
  const bytes = readFileSync(new URL('../public/media/avatar/moalim-professeur.glb', import.meta.url));
  assert.equal(bytes.toString('ascii', 0, 4), 'glTF');
  const jsonLength = bytes.readUInt32LE(12);
  const model = JSON.parse(bytes.toString('utf8', 20, 20 + jsonLength).trim());
  const names = new Set(model.nodes.map(node => node.name));
  for (const side of ['Left', 'Right']) {
    for (const name of ['Shoulder', 'Arm', 'ForeArm', 'Hand'])
      assert.ok(names.has(side + name), side + name);
    for (const finger of ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'])
      for (const k of [1, 2, 3]) assert.ok(names.has(`${side}Hand${finger}${k}`), `${side}Hand${finger}${k}`);
  }
  for (const name of ['Hips', 'Spine2', 'Neck', 'Head']) assert.ok(names.has(name), name);
  assert.ok(model.skins?.length, 'body is rigged');
  assert.ok(model.animations?.some(clip => /idle/i.test(clip.name)), 'idle clip is included');
  assert.ok(!model.buffers.some(buffer => buffer.uri), 'GLB is self-contained');
  assert.ok(bytes.length < 8e6, 'GLB stays light enough for the session page');
});

