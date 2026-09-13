import assert from 'node:assert/strict';
import { evaluateMathExpression } from '../src/utils/mathExpression.ts';

for (const [expression, x, expected] of [
  ['x^2 + 2*x + 1', 2, 9], ['-x^2', 3, -9], ['2^3^2', 0, 512],
  ['sin(pi/2)', 0, 1], ['sqrt(abs(-9))', 0, 3], ['Math.cos(0)', 0, 1],
  ['1e-3 * x', 1000, 1], ['max(2, x)', 3, 3], ['2^-2', 0, 0.25],
]) assert.equal(evaluateMathExpression(expression, x), expected, expression);

for (const expression of [
  'globalThis.process.exit()', 'x.constructor.constructor("return process")()',
  'alert(1)', '(function(){return 1})()', '(()=>1)()', 'x=4', 'x;1',
  '[1][0]', 'constructor(1)', '__proto__(1)', '1/0', 'sqrt(-1)', 'sin(x',
  '1 '.repeat(300), 'x'.repeat(513),
]) assert.equal(evaluateMathExpression(expression, 1), null, expression);
console.log('24 mathematical expression and script-injection checks passed');
