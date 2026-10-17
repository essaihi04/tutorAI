import { audioUnlock } from './audioUnlock';
import { LipSyncAnalyser } from '../vendor/three-ws/lip-sync-analyser.js';

// A single analysis bus observes the existing playback clock, including scheduled PCM.
// It is never connected to destination: the original audio plays exactly once.
let analyser: AnalyserNode | null = null;
const lips = new LipSyncAnalyser();
const attached = new WeakSet<HTMLMediaElement>();
const waveform = new Float32Array(1024);
let envelope = 0;
let lastSample = 0;

function bus(context: AudioContext) {
  if (!analyser) {
    analyser = context.createAnalyser();
    analyser.fftSize = 1024;
    analyser.smoothingTimeConstant = 0.35;
    lips.connect(analyser);
  }
  return analyser;
}

export function observeAvatarSource(source: AudioNode) {
  const context = audioUnlock.context();
  if (!context || source.context !== context) return;
  source.connect(bus(context));
}

export function observeAvatarMedia(media: HTMLMediaElement) {
  if (attached.has(media)) return;
  // Never reroute a cross-origin recording without CORS: Web Audio would mute it.
  const url = new URL(media.src, location.href);
  if (!['blob:', 'data:'].includes(url.protocol) && url.origin !== location.origin) return;
  attached.add(media);
  let source: MediaElementAudioSourceNode | null = null;
  let connected = false;
  const attach = () => {
    const context = audioUnlock.context();
    if (!context || context.state !== 'running' || connected) return;
    try {
      source ||= context.createMediaElementSource(media);
      source.connect(context.destination);
      observeAvatarSource(source);
      connected = true;
    } catch { /* Keep playback independent of avatar support. */ }
  };
  media.addEventListener('playing', attach);
  const disconnect = () => { source?.disconnect(); connected = false; };
  media.addEventListener('pause', disconnect);
  media.addEventListener('ended', disconnect);
  media.addEventListener('error', disconnect);
}

export function sampleAvatarAudio() {
  const weights = lips.sample() || {};
  const now = performance.now();
  const dt = Math.min(.1, Math.max(0, (now - lastSample) / 1000));
  lastSample = now;
  let energy = 0;
  if (analyser && analyser.context.state === 'running') {
    analyser.getFloatTimeDomainData(waveform);
    for (const value of waveform) energy += value * value;
  }
  // Waveform RMS follows syllables and closures faster than smoothed FFT magnitude.
  const rms = Math.sqrt(energy / waveform.length);
  const target = Math.min(1, Math.max(0, rms - .003) * 7);
  envelope += (target - envelope) * (1 - Math.exp(-dt / (target > envelope ? .025 : .055)));
  // Le bus d'analyse voit le son avant sa sortie au haut-parleur : la latence permet de s'y caler.
  const context = analyser?.context as (AudioContext & { outputLatency?: number }) | undefined;
  const latency = context ? (context.outputLatency || 0) + (context.baseLatency || 0) : 0;
  return { weights, amplitude: envelope, rms, latency };
}
