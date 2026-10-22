import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  PHASES, PROTOCOL, COMPOSITION, assessOrder, generateField, counts, assessIdentification,
  mitoticIndex, assessIndex, phaseDuration, assessDuration, dnaQuantity, assessDna,
} from '../public/media/simulations/svt/ch2_information_genetique/mitose/model.js';

test('le protocole juste est accepté, une inversion reçoit son message', () => {
  assert.equal(assessOrder(PROTOCOL.map(s => s.id)).correct, true);
  const r = assessOrder(['prelever', 'fixer', 'colorer']);
  assert.equal(r.correct, false);
  assert.equal(r.position, 2);
  assert.match(r.reason, /hydrolyse/);
  assert.match(assessOrder(['prelever', 'fixer']).reason, /manque/);
});

test('le champ est reproductible et respecte la composition', () => {
  const a = generateField(7), b = generateField(7), c = generateField(8);
  assert.deepEqual(a.cells.map(x => x.phase), b.cells.map(x => x.phase));
  assert.notDeepEqual(a.cells.map(x => x.phase), c.cells.map(x => x.phase));
  assert.deepEqual(counts(a), COMPOSITION);
  assert.equal(a.cells.length, 48);
});

test('cinq cellules repérées, une par phase', () => {
  const f = generateField(7);
  assert.equal(new Set(f.marked).size, 5);
  assert.deepEqual(f.marked.map(i => f.cells[i].phase).sort(), [...PHASES].sort());
});

test('les confusions classiques reçoivent un indice ciblé', () => {
  assert.equal(assessIdentification('metaphase', 'metaphase').correct, true);
  // Répondre « métaphase » devant une anaphase : on fait chercher les deux groupes.
  assert.match(assessIdentification('anaphase', 'metaphase').reason, /deux groupes/);
  // Répondre « interphase » devant une télophase : on fait compter les noyaux.
  assert.match(assessIdentification('telophase', 'interphase').reason, /deux noyaux/);
  assert.match(assessIdentification('interphase', 'telophase').reason, /Combien de noyaux/);
});

test('indice mitotique : 14 / 48 × 100, avec les pièges', () => {
  const c = counts(generateField(7));
  assert.ok(Math.abs(mitoticIndex(c) - 29.17) < 0.01);
  assert.equal(assessIndex('29,2', c).correct, true);
  assert.equal(assessIndex('29 %', c).correct, true);
  assert.match(assessIndex('0,29', c).reason, /fraction/);
  assert.match(assessIndex('41,2', c).reason, /TOTAL/);
});

test('durée d’une phase proportionnelle à sa fréquence', () => {
  const c = counts(generateField(7));
  assert.equal(phaseDuration(c, 'metaphase', 20), 75);
  assert.equal(assessDuration('75', c, 'metaphase', 20).correct, true);
  assert.match(assessDuration('1,25', c, 'metaphase', 20).reason, /heures/);
  assert.match(assessDuration(String(3 / 14 * 20 * 60), c, 'metaphase', 20).reason, /total/);
});

test('l’ADN double en phase S et revient à q après la mitose', () => {
  assert.equal(dnaQuantity(0.1), 1);
  assert.equal(dnaQuantity(0.8), 2);
  assert.equal(dnaQuantity(0.99), 1);
  assert.equal(assessDna('cycle').correct, true);
  assert.match(assessDna('halved').reason, /prophase/);
});
