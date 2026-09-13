import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import ts from 'typescript';

const source = await readFile(new URL('../src/components/session/scientific/energyBalanceModel.ts', import.meta.url), 'utf8');
const compiled = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
const { energyBalance, energyPhase, ENERGY_PHASES, energyExplanation, energyNumber } = await import(`data:text/javascript;base64,${Buffer.from(compiled).toString('base64')}`);

test('38 ATP : 4 directs + 34 chaîne, sans double comptage', () => {
  const b = energyBalance('scene');
  assert.equal(b.nadhATP, 30);
  assert.equal(b.fadh2ATP, 4);
  assert.equal(b.chainATP, 34);
  assert.equal(b.totalATP, b.glycolysisATP + b.matrixATP + b.chainATP);
  assert.equal(b.totalATP, 38);
  assert.equal(b.respirationEnergy, 1159);
  assert.equal(energyNumber(b.respirationPercent, 1), '40,5');
});
test('la navette 36 modifie uniquement le rendement des NADH cytoplasmiques', () => {
  const a = energyBalance('scene'); const b = energyBalance('navette_36');
  assert.equal(b.chainATP, 32);
  assert.equal(b.nadhATP, 28);
  assert.equal(b.totalATP, 36);
  assert.equal(b.glycolysisATP, a.glycolysisATP);
  assert.equal(b.matrixATP, a.matrixATP);
  assert.equal(b.respirationEnergy, 1098);
  assert.equal(energyNumber(b.respirationPercent, 1), '38,4');
});
test('fermentation : 2 ATP, 61 kJ, 2,13 % sur la même échelle', () => {
  for (const variant of ['scene', 'navette_36']) {
    const b = energyBalance(variant);
    assert.equal(b.glucoseEnergy, 2860);
    assert.equal(b.fermentationEnergy, 61);
    assert.equal(energyNumber(b.fermentationPercent, 2), '2,13');
    assert.ok(b.respirationPercent < 100);
  }
});
test('les 11 pas remplacent le dessin dans cinq vues, sans accumuler le texte', () => {
  assert.deepEqual(Array.from({ length: 11 }, (_, i) => energyPhase(i)), [0,0,0,1,1,1,2,2,3,4,4]);
  for (const [i, phase] of ENERGY_PHASES.entries()) assert.equal(energyPhase(phase.step), i);
  assert.equal(energyPhase(-3), 0);
  assert.equal(energyPhase(100), 4);
  assert.equal(energyPhase(NaN), 0);
});
test('les détails conservent les nuances scientifiques', () => {
  assert.match(energyExplanation(1, 'scene'), /oxydation.*pyruvates.*Krebs/);
  assert.match(energyExplanation(2, 'scene'), /10 NADH \(2 \+ 8\)/);
  assert.match(energyExplanation(2, 'navette_36'), /32 ATP/);
  assert.match(energyExplanation(3, 'scene'), /Ne pas ajouter/);
  assert.match(energyExplanation(4, 'scene'), /produits organiques/);
  assert.deepEqual(energyBalance('unknown'), energyBalance('scene'));
});
