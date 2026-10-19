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
test('distributed GLB is a light, self-contained professor rig with idle, talking and a moustache', () => {
  const bytes = readFileSync(new URL('../public/media/avatar/moalim-professeur.glb', import.meta.url));
  assert.equal(bytes.toString('ascii', 0, 4), 'glTF');
  const jsonLength = bytes.readUInt32LE(12);
  const model = JSON.parse(bytes.toString('utf8', 20, 20 + jsonLength).trim());
  const names = new Set(model.nodes.map(node => node.name));
  for (const side of ['Left', 'Right']) {
    for (const name of ['Shoulder', 'Arm', 'ForeArm', 'Hand', 'UpLeg', 'Leg'])
      assert.ok(names.has(side + name), side + name);
    for (const finger of ['Thumb', 'Index', 'Middle', 'Pinky'])
      for (const k of [1, 2, 3]) assert.ok(names.has(`${side}Hand${finger}${k}`), `${side}Hand${finger}${k}`);
  }
  for (const name of ['Hips', 'Head', 'Moustache', 'BrowLeft', 'BrowRight']) assert.ok(names.has(name), name);
  assert.ok(model.skins?.length, 'body is rigged');
  const clips = model.animations?.map(clip => clip.name) ?? [];
  for (const clip of ['Idle', 'Talking']) assert.ok(clips.includes(clip), clip);
  const targets = new Set(model.meshes.flatMap(mesh => mesh.extras?.targetNames ?? []));
  for (const name of ['eyesClosed', 'lookLeft', 'lookRight', 'lookUp', 'lookDown']) assert.ok(targets.has(name), `morph target ${name}`);
  assert.ok(!model.buffers.some(buffer => buffer.uri), 'GLB is self-contained');
  assert.ok(bytes.length < 3e6, 'GLB stays light for the session page');
});
test('the talking gestures never snap an arm into place from one frame to the next', () => {
  const bytes = readFileSync(new URL('../public/media/avatar/moalim-professeur.glb', import.meta.url));
  const jsonLength = bytes.readUInt32LE(12);
  const model = JSON.parse(bytes.toString('utf8', 20, 20 + jsonLength).trim());
  const bin = bytes.subarray(20 + jsonLength + 8);
  const read = index => {
    const accessor = model.accessors[index], view = model.bufferViews[accessor.bufferView];
    const width = { SCALAR: 1, VEC4: 4 }[accessor.type], start = (view.byteOffset ?? 0) + (accessor.byteOffset ?? 0);
    return Array.from({ length: accessor.count }, (_, i) => Array.from({ length: width }, (_, k) => bin.readFloatLE(start + 4 * (i * width + k))));
  };
  const talking = model.animations.find(clip => clip.name === 'Talking');
  let fastest = 0;
  for (const channel of talking.channels) {
    if (channel.target.path !== 'rotation' || !/Arm|ForeArm|Hand$/.test(model.nodes[channel.target.node].name)) continue;
    const sampler = talking.samplers[channel.sampler], times = read(sampler.input), rotations = read(sampler.output);
    for (let i = 1; i < rotations.length; i++) {
      const dot = Math.abs(rotations[i].reduce((sum, value, k) => sum + value * rotations[i - 1][k], 0));
      fastest = Math.max(fastest, (2 * Math.acos(Math.min(1, dot)) * 180 / Math.PI) / (times[i][0] - times[i - 1][0]));
    }
  }
  assert.ok(fastest < 480, `arms turn at most ${fastest.toFixed(0)}°/s (8° per frame at 60 fps)`);
});
