import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { SyllableEnvelope } from '../src/services/syllableEnvelope.js';

const FPS = 60;
const AUDIO = new URL('../public/media/audio/courses/svt_ch1_energy/fr/', import.meta.url);

function readWav(url) {
  const b = readFileSync(url);
  let o = 12, fmt = null, data = null;
  while (o < b.length) {
    const id = b.toString('ascii', o, o + 4), size = b.readUInt32LE(o + 4);
    if (id === 'fmt ') fmt = { ch: b.readUInt16LE(o + 10), rate: b.readUInt32LE(o + 12), bits: b.readUInt16LE(o + 22) };
    if (id === 'data') data = b.subarray(o + 8, o + 8 + size);
    o += 8 + size + (size % 2);
  }
  const n = data.length / (fmt.bits / 8) / fmt.ch, samples = new Float32Array(n);
  for (let i = 0; i < n; i++) samples[i] = fmt.bits === 16 ? data.readInt16LE(i * 2 * fmt.ch) / 32768 : data.readFloatLE(i * 4 * fmt.ch);
  return { rate: fmt.rate, samples };
}

/** RMS sur ~21 ms (la fenêtre du bus d'analyse du navigateur), 60 fois par seconde. */
function rmsFrames({ rate, samples }) {
  const hop = Math.round(rate / FPS), win = Math.round(rate * 0.021), out = [];
  for (let i = 0; i + win < samples.length; i += hop) {
    let e = 0;
    for (let k = i; k < i + win; k++) e += samples[k] * samples[k];
    out.push(Math.sqrt(e / win));
  }
  return out;
}

function openings(series) {
  let cycles = 0, armed = true;
  for (const v of series) {
    if (armed && v > 0.6) { cycles++; armed = false; } else if (!armed && v < 0.3) armed = true;
  }
  return cycles / (series.length / FPS);
}

test('the moustache opens and closes with the syllables of real course recordings', () => {
  const files = readdirSync(AUDIO).filter(name => name.endsWith('.wav')).slice(0, 3);
  assert.ok(files.length >= 2, 'course recordings are available');
  for (const name of files) {
    const frames = rmsFrames(readWav(new URL(name, AUDIO)));
    const env = new SyllableEnvelope();
    const series = frames.map((rms, f) => env.push(rms, 1 / FPS, f / FPS));
    const speaking = series.filter(v => v > 0.05).length;
    assert.ok(openings(series) >= 2, `${name}: ${openings(series).toFixed(2)} openings/s`);
    assert.ok(series.filter(v => v > 0.95).length / speaking < 0.3, `${name}: not stuck wide open`);
    assert.ok(Math.max(...series) > 0.9, `${name}: opens fully on stressed syllables`);
    const jump = Math.max(...series.slice(1).map((v, f) => Math.abs(v - series[f])));
    assert.ok(jump <= 0.2, `${name}: moves smoothly from frame to frame (largest step ${jump.toFixed(2)})`);
  }
});

test('silence closes the mouth and the output latency delays the motion', () => {
  const env = new SyllableEnvelope();
  for (let f = 0; f < 30; f++) env.push(0, 1 / FPS, f / FPS);
  assert.equal(env.open, 0);
  const late = new SyllableEnvelope(), early = new SyllableEnvelope();
  let firstLate = null, firstEarly = null;
  for (let f = 0; f < 60; f++) {
    const rms = f < 20 ? 0.001 : 0.004 + 0.12 * (f % 8 < 4 ? 1 : 0.2);   // silence, then pulsed syllables
    if (late.push(rms, 1 / FPS, f / FPS, 0.1) > 0.5 && firstLate === null) firstLate = f;
    if (early.push(rms, 1 / FPS, f / FPS, 0) > 0.5 && firstEarly === null) firstEarly = f;
  }
  assert.ok(firstEarly !== null && firstLate !== null);
  assert.ok(firstLate - firstEarly >= 5, `latency of 100 ms delays the opening by ~6 frames (${firstLate - firstEarly})`);
});
