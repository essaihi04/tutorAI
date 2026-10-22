import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  tau, chargeVoltage, dischargeVoltage, current, energy, tangentAtOrigin, reading,
  percentError, assessPrediction, assessTau, assessCapacitance, duration,
} from '../public/media/simulations/physics/tp/rc/model.js';

test('τ = R·C, avec C en µF', () => {
  assert.equal(tau(1000, 100), 0.1);
  assert.ok(Math.abs(tau(2200, 470) - 1.034) < 1e-12);
  assert.throws(() => tau(0, 100));
});

test('à t = τ, la charge atteint 63 % de E et la décharge 37 % de U₀', () => {
  const t = tau(1000, 470);
  assert.ok(Math.abs(chargeVoltage(6, t, t) / 6 - 0.632) < 1e-3);
  assert.ok(Math.abs(dischargeVoltage(6, t, t) / 6 - 0.368) < 1e-3);
  assert.ok(chargeVoltage(6, t, duration(t)) > 0.99 * 6);
  assert.equal(chargeVoltage(6, t, 0), 0);
});

test('la tangente à l’origine coupe u = E à t = τ', () => {
  const t = tau(1000, 470);
  assert.ok(Math.abs(tangentAtOrigin(6, t, t) - 6) < 1e-12);
});

test('le courant s’annule en fin de charge et change de signe à la décharge', () => {
  const t = tau(1000, 100);
  assert.ok(Math.abs(current('charge', 6, 1000, t, 0) - 6) < 1e-12);
  assert.ok(current('charge', 6, 1000, t, duration(t)) < 0.05);
  assert.ok(current('discharge', 6, 1000, t, 0) < 0);
});

test('énergie ½·C·u² en mJ', () => {
  assert.ok(Math.abs(energy(1000, 6) - 18) < 1e-9);
});

test('les lectures sont proches du modèle, arrondies à 0,01 V, et reproductibles', () => {
  for (let s = 0; s < 50; s++) {
    const r = reading(3.456, s);
    assert.ok(Math.abs(r - 3.456) <= 0.0151, 'bruit ±0,01 V + arrondi ±0,005 V');
    assert.ok(Math.abs(r * 100 - Math.round(r * 100)) < 1e-9);
    assert.equal(reading(3.456, s), r);
  }
});

test('la prédiction juste est « τ double »', () => {
  assert.equal(assessPrediction('double').correct, true);
  assert.equal(assessPrediction('same').correct, false);
});

test('la lecture de τ est acceptée à 5 %, avec des messages ciblés', () => {
  const t = 0.47;
  assert.equal(assessTau('0,47', t, 'percent').correct, true);
  assert.equal(assessTau(0.49, t, 'tangent').correct, true);
  assert.equal(assessTau(0.52, t, 'percent').correct, false);
  assert.match(assessTau(470, t, 'percent').reason, /millisecondes/);
  assert.match(assessTau(0.3, t, 'discharge').reason, /0,37/);
  assert.match(assessTau('abc', t, 'percent').reason, /positive/);
});

test('C = τ / R en µF, avec le piège des farads', () => {
  assert.equal(assessCapacitance('470', 0.47, 1000, 470).correct, true);
  assert.match(assessCapacitance('0,00047', 0.47, 1000, 470).reason, /farads/);
  assert.equal(assessCapacitance('47', 0.47, 1000, 470).correct, false);
  assert.ok(percentError(480, 470) > 2 && percentError(480, 470) < 2.2);
});
