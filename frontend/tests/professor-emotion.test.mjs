import test from 'node:test';
import assert from 'node:assert/strict';
import { PROFESSOR_EMOTIONS, REPONSE_ELEVE_EVENT, detectProfessorEmotion, signalerReponseEleve } from '../src/services/professorEmotion.js';

test('the tutor\'s words give the professor an emotion', () => {
  assert.equal(detectProfessorEmotion('Bonjour Amine ! Prêt pour les ondes ?'), 'greet');
  assert.equal(detectProfessorEmotion('Salam ! On reprend la corde.'), 'greet');
  assert.equal(detectProfessorEmotion('Bravo, c’est exactement ça !'), 'celebrate');
  assert.equal(detectProfessorEmotion('Mabrouk, très bien vu.'), 'celebrate');
  assert.equal(detectProfessorEmotion('Je suis fier de toi ❤️'), 'love');
  assert.equal(detectProfessorEmotion('Pas tout à fait : réessaie en regardant le point orange.'), 'encourage');
  assert.equal(detectProfessorEmotion('Au revoir, à bientôt pour la suite !'), 'goodbye');
  assert.equal(detectProfessorEmotion('Haha, c’est drôle, mais non : la corde ne voyage pas.'), 'laugh');
  assert.equal(detectProfessorEmotion('Oh ! Incroyable, tu as vu la double amplitude ?'), 'surprise');
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
  assert.equal(detectProfessorEmotion('hahaha trop fort', 'student'), 'laugh');
  assert.equal(detectProfessorEmotion('wow 😮', 'student'), 'surprise');
  assert.equal(detectProfessorEmotion('c’est quoi une onde ?', 'student'), null);
  assert.equal(detectProfessorEmotion('', 'student'), null);
});

test('every emotion has emojis and a known gesture', () => {
  for (const [kind, spec] of Object.entries(PROFESSOR_EMOTIONS)) {
    assert.ok(spec.emojis.length >= 1 && spec.count >= 1, kind);
    assert.ok([null, 'wave', 'cheer', 'heart', 'nod', 'laugh', 'startle', 'shake'].includes(spec.gesture), kind);
  }
});

test('an answer on the board reaches the professor, right or wrong', () => {
  const recu = [];
  globalThis.window = new EventTarget();
  try {
    window.addEventListener(REPONSE_ELEVE_EVENT, event => recu.push(event.detail.juste));
    signalerReponseEleve(true);
    signalerReponseEleve(false);
  } finally {
    delete globalThis.window;
  }
  assert.deepEqual(recu, [true, false]);
});

test('a judged answer gives the professor a gesture: bravo, no of the head, or a nod', async () => {
  const { emotionPourReponse, emotionPourEvaluation } = await import('../src/services/professorEmotion.js');
  assert.equal(emotionPourReponse(true), 'celebrate');
  assert.equal(emotionPourReponse(false), 'wrong');
  assert.equal(PROFESSOR_EMOTIONS.wrong.gesture, 'shake');
  assert.equal(emotionPourEvaluation('correct'), 'celebrate');
  assert.equal(emotionPourEvaluation('faux'), 'wrong');
  assert.equal(emotionPourEvaluation('partiel'), 'encourage');
  assert.equal(emotionPourEvaluation('incertain'), null);
  assert.equal(emotionPourEvaluation('aucune'), null);
});
