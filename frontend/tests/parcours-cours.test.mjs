import test from 'node:test';
import assert from 'node:assert/strict';
import {
  clesDesQuestions, rejeuDe, rejeuxDe, momentsDuRejeu, momentsReserves, commandeReservee, dureeDuRejeuMs, questionClose,
  diagnosticsDuRappel, justeDuPremierCoup, rappelASauter, diapoSuivante,
} from '../src/components/course/parcours.js';

// ── 1. Rejouer la simulation après la réponse ──
const x1 = {
  id: 'pr_x1', title: 'x1',
  question: { prompt: 'H′(x) ?', options: ['a', 'b', 'c'], correct: 0 },
  exercises: [{ type: 'vrai_faux', prompt: 'p', statements: [{ text: 's0', correct: true }, { text: 's1', correct: false }] }],
  concentration: {
    pointage: [{ mot: 'السطر اللول:', commande: 'play_until', parametres: { moment: 'derivable' } }],
    apres_reponse: { etapes: [{ commande: 'play_until', parametres: { moment: 'calcul' } }, { repere: 'calcul' }] },
  },
};

test('les clés des questions suivent le tableau : q, puis e{i}, e{i}s{j}', () => {
  assert.deepEqual(clesDesQuestions(x1), ['q', 'e0s0', 'e0s1']);
  assert.deepEqual(clesDesQuestions({ exercises: [{ type: 'qcm', choices: ['a', 'b'] }, { type: 'association' }] }), ['e0']);
  assert.deepEqual(clesDesQuestions({}), []);
});

test('le rejeu : la première question par défaut, 6 s par défaut, moments réservés', () => {
  const r = rejeuDe(x1);
  assert.equal(r.question, 'q');
  assert.equal(r.duree_s, 6);
  assert.equal(dureeDuRejeuMs(r), 7000, 'une seconde de plus pour le second geste');
  assert.deepEqual([...momentsReserves(x1)], ['calcul']);
  assert.ok(commandeReservee('play_until', { moment: 'calcul' }, momentsReserves(x1)));
  assert.ok(!commandeReservee('play_until', { moment: 'derivable' }, momentsReserves(x1)));
  assert.ok(!commandeReservee('highlight', { moment: 'calcul' }, momentsReserves(x1)));
});

test('le rejeu peut viser une autre question et garder la simulation muette avant', () => {
  const s = { ...x1, concentration: { apres_reponse: { question: 'e0s1', duree_s: 3, sim_avant: { conclusions: false }, etapes: [{ commande: 'set_parameters', parametres: { conclusions: true } }] } } };
  const r = rejeuDe(s);
  assert.equal(r.question, 'e0s1');
  assert.equal(r.duree_s, 3);
  assert.deepEqual(r.sim_avant, { conclusions: false });
  assert.equal(momentsReserves(s).size, 0);
});

test('sans le format, ou mal écrit, rien ne change', () => {
  assert.equal(rejeuDe({ ...x1, concentration: {} }), null);
  assert.equal(rejeuDe({ ...x1, concentration: { apres_reponse: { etapes: [] } } }), null);
  assert.equal(rejeuDe({ ...x1, concentration: { apres_reponse: { question: 'e5', etapes: [{ repere: 'a' }] } } }), null, 'question inconnue');
  assert.equal(rejeuDe({ id: 'v', concentration: { apres_reponse: { etapes: [{ repere: 'a' }] } } }), null, 'diapositive sans question');
  assert.equal(momentsReserves({ concentration: {} }).size, 0);
  assert.ok(!commandeReservee('play_until', { moment: 'calcul' }, new Set()));
});

test('une liste : un rejeu par question (maths ch4, x1 : q → derivee, e0 → calcul et conclusion)', () => {
  const s = { ...x1, exercises: [{ type: 'qcm', prompt: 'p', choices: ['a', 'b', 'c'], correct: 0 }], concentration: { apres_reponse: [
    { etapes: [{ commande: 'play_until', parametres: { moment: 'derivee' } }] },
    { question: 'e0', etapes: [{ commande: 'play_until', parametres: { moment: 'calcul' } }, { commande: 'play_until', parametres: { moment: 'conclusion' } }] },
    { etapes: [{ repere: 'sans_question' }] },                                  // sans `question` après le premier : ignoré
    { question: 'q', etapes: [{ repere: 'doublon' }] },                          // même question : le premier compte
  ] } };
  assert.deepEqual(rejeuxDe(s).map(r => r.question), ['q', 'e0']);
  assert.equal(rejeuDe(s, 'e0').etapes.length, 2);
  assert.equal(rejeuDe(s, 'e1'), null);
  assert.deepEqual([...momentsDuRejeu(rejeuDe(s, 'e0'))], ['calcul', 'conclusion']);
  assert.deepEqual([...momentsReserves(s)].sort(), ['calcul', 'conclusion', 'derivee']);
  assert.deepEqual([...momentsReserves(s, new Set(['q']))].sort(), ['calcul', 'conclusion'], 'q répondue : derivee est libre');
});

test('une question close en mémoire : juste, fausse après ses essais, ou passée', () => {
  assert.ok(questionClose({ retour: { correct: true }, tentative: 1 }));
  assert.ok(questionClose({ retour: { correct: false }, tentative: 3 }));
  assert.ok(!questionClose({ retour: { correct: false }, tentative: 2 }), 'il lui reste un essai');
  assert.ok(questionClose({ passee: true }));
  assert.ok(!questionClose({}));
  assert.ok(!questionClose(null));
});

// ── 2. Sauter un rappel déjà su ──
const cours = [
  { id: 'le_o1' },
  { id: 'le_o2_acquis', question: { prompt: 'D’où vient la matière organique ?', options: ['a', 'b', 'c'], correct: 1 } },
  { id: 'le_p1_cellule', concentration: { rappel: { si_reussi: 'le_o2_acquis' } } },
  { id: 'le_p2_glucose', question: { prompt: 'énergie ?', options: ['a', 'b', 'c'], correct: 2 }, concentration: { rappel: { si_reussi: ['le_o2_acquis'] } } },
  { id: 'le_a1_monnaie' },
];
const memoire = etats => (slideId, cle) => etats[`${slideId}:${cle}`];

test('un rappel nomme son diagnostic (un id ou une liste)', () => {
  assert.deepEqual(diagnosticsDuRappel(cours[2]), ['le_o2_acquis']);
  assert.deepEqual(diagnosticsDuRappel(cours[3]), ['le_o2_acquis']);
  assert.deepEqual(diagnosticsDuRappel(cours[0]), []);
  assert.deepEqual(diagnosticsDuRappel({ concentration: { rappel: {} } }), []);
});

test('juste du premier coup seulement', () => {
  assert.ok(justeDuPremierCoup({ retour: { correct: true } }));
  assert.ok(justeDuPremierCoup({ retour: { correct: true }, tentative: 1 }));
  assert.ok(!justeDuPremierCoup({ retour: { correct: true }, tentative: 2 }), 'juste après l’indice');
  assert.ok(!justeDuPremierCoup({ retour: { correct: false }, tentative: 3 }));
  assert.ok(!justeDuPremierCoup({ passee: true }));
  assert.ok(!justeDuPremierCoup(undefined));
});

test('diagnostic réussi du premier coup : les deux rappels sont sautés', () => {
  const lire = memoire({ 'le_o2_acquis:q': { retour: { correct: true }, tentative: 1 } });
  assert.deepEqual(diapoSuivante(cours, 1, lire), { index: 4, sautes: ['le_p1_cellule', 'le_p2_glucose'] });
});

test('diagnostic raté, réussi au 2e essai, passé ou pas fait : le rappel est joué', () => {
  for (const etat of [{ retour: { correct: false }, tentative: 3 }, { retour: { correct: true }, tentative: 2 }, { passee: true }, undefined]) {
    assert.deepEqual(diapoSuivante(cours, 1, memoire({ 'le_o2_acquis:q': etat })), { index: 2, sautes: [] });
  }
});

test('un diagnostic sans question ou introuvable ne fait jamais sauter', () => {
  const sansQuestion = [{ id: 'd' }, { id: 'r', concentration: { rappel: { si_reussi: 'd' } } }, { id: 'n' }];
  assert.deepEqual(diapoSuivante(sansQuestion, 0, () => ({ retour: { correct: true } })), { index: 1, sautes: [] });
  const introuvable = [{ id: 'a' }, { id: 'r', concentration: { rappel: { si_reussi: 'zzz' } } }];
  assert.deepEqual(diapoSuivante(introuvable, 0, () => ({ retour: { correct: true } })), { index: 1, sautes: [] });
});

test('toutes les questions de tous les diagnostics doivent être justes du premier coup', () => {
  const d = [
    { id: 'd1', question: { prompt: 'q', options: ['a', 'b'] }, exercises: [{ type: 'qcm', choices: ['a', 'b'] }] },
    { id: 'd2', question: { prompt: 'q2' } },
    { id: 'r', concentration: { rappel: { si_reussi: ['d1', 'd2'] } } },
    { id: 'n' },
  ];
  const juste = { retour: { correct: true }, tentative: 1 };
  assert.equal(rappelASauter(d[2], new Map(d.map(s => [s.id, s])), memoire({ 'd1:q': juste, 'd2:q': juste })), false, 'e0 de d1 manque');
  assert.equal(rappelASauter(d[2], new Map(d.map(s => [s.id, s])), memoire({ 'd1:q': juste, 'd1:e0': juste, 'd2:q': juste })), true);
  assert.deepEqual(diapoSuivante(d, 1, memoire({ 'd1:q': juste, 'd1:e0': juste, 'd2:q': juste })), { index: 3, sautes: ['r'] });
});

test('un rappel demandé (« Revoir le rappel ») n’est plus sauté ; un rappel en fin de cours mène à la fin', () => {
  const lire = memoire({ 'le_o2_acquis:q': { retour: { correct: true }, tentative: 1 } });
  assert.deepEqual(diapoSuivante(cours, 1, lire, new Set(['le_p1_cellule', 'le_p2_glucose'])), { index: 2, sautes: [] });
  assert.deepEqual(diapoSuivante(cours, 2, lire, new Set(['le_p1_cellule'])), { index: 4, sautes: ['le_p2_glucose'] });
  const fin = [cours[1], cours[2]];
  assert.deepEqual(diapoSuivante(fin, 0, lire), { index: 2, sautes: ['le_p1_cellule'] });
});

test('un cours sans rappel avance d’une diapositive, comme avant', () => {
  const simple = [{ id: 'a' }, { id: 'b', question: { prompt: 'x' } }, { id: 'c' }];
  for (let i = 0; i < 3; i++) assert.deepEqual(diapoSuivante(simple, i, () => ({ retour: { correct: true } })), { index: i + 1, sautes: [] });
});
