import test from 'node:test';
import assert from 'node:assert/strict';
import { boardExplaining } from '../src/services/boardExplaining.js';

test('the professor explains while a board script runs, with or without a voice', () => {
  const seen = [];
  const unsubscribe = boardExplaining.subscribe(value => seen.push(value));
  assert.equal(boardExplaining.active, false);
  const first = boardExplaining.begin();
  const second = boardExplaining.begin();
  assert.equal(boardExplaining.active, true);
  first(); first();
  assert.equal(boardExplaining.active, true, 'releasing twice never frees another holder');
  second();
  assert.equal(boardExplaining.active, false);
  assert.deepEqual(seen, [true, false], 'one start and one stop, no flicker in between');
  unsubscribe();
});
