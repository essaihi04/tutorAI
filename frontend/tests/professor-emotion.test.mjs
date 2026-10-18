import test from 'node:test';
import assert from 'node:assert/strict';
import { PROFESSOR_EMOTIONS, detectProfessorEmotion } from '../src/services/professorEmotion.js';

test('the tutor\'s words give the professor an emotion', () => {
  assert.equal(detectProfessorEmotion('Bonjour Amine ! Prêt pour les ondes ?'), 'greet');
  assert.equal(detectProfessorEmotion('Salam ! On reprend la corde.'), 'greet');
  assert.equal(detectProfessorEmotion('Bravo, c’est exactement ça !'), 'celebrate');
  assert.equal(detectProfessorEmotion('Mabrouk, très bien vu.'), 'celebrate');
  assert.equal(detectProfessorEmotion('Je suis fier de toi ❤️'), 'love');
  assert.equal(detectProfessorEmotion('Pas tout à fait : réessaie en regardant le point orange.'), 'encourage');
  assert.equal(detectProfessorEmotion('Au revoir, à bientôt pour la suite !'), 'goodbye');
  assert.equal(detectProfessorEmotion('La célérité vaut v = √(T/μ).'), null);
  assert.equal(detectProfessorEmotion('Ce n’est pas un bonjour : la vitesse ne change pas.'), null, 'a greeting only counts at the start');
});

test('celebration wins over encouragement in the same reply', () => {
  assert.equal(detectProfessorEmotion('Bravo ! Presque parfait, on continue.'), 'celebrate');
});

test('the student\'s words too: thanks, hello, goodbye', () => {
  assert.equal(detectProfessorEmotion('merci prof !', 'student'), 'love');
  assert.equal(detectProfessorEmotion('salut', 'student'), 'greet');
  assert.equal(detectProfessorEmotion('bslama', 'student'), 'goodbye');
  assert.equal(detectProfessorEmotion('c’est quoi une onde ?', 'student'), null);
  assert.equal(detectProfessorEmotion('', 'student'), null);
});

test('every emotion has emojis and a known gesture', () => {
  for (const [kind, spec] of Object.entries(PROFESSOR_EMOTIONS)) {
    assert.ok(spec.emojis.length >= 1 && spec.count >= 1, kind);
    assert.ok([null, 'wave', 'cheer', 'heart', 'nod'].includes(spec.gesture), kind);
  }
});
