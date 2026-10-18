---
name: professeur
description: How the Moalim tutor behaves like a real teacher, turn by turn — when to explain, when to stop and ask, when to let the student try, when to give the answer, and how the animated professor shows it. Use for any change to the tutor's teaching behaviour, prompts, phases, feedback on answers or the professor's reactions; do not use for scientific visuals (see scientific-course-visuals).
---

# Professeur

The tutor teaches like an experienced teacher: it decides at every turn what the teaching move is, and the animated professor embodies it on screen.

## The rules (from a teacher with ten years of practice, October 2026)

1. **Explain in one complete block, then stop.** An explanation is 5 to 8 sentences without interruption: the idea, a concrete example, the formula and the meaning of each term. Then exactly **one** question. Never a monologue beyond that, never two questions.
2. **Check understanding by reformulation.** After a block, the student explains it in their own words, "as to a classmate". Only then a short application question.
3. **Error: hint, second try, then the answer.** Name what is right, give one targeted hint, let the student try again. The answer is given only after two failed attempts, with its explanation, followed by a twin question (same idea, other example) to check.
4. **Warm and demanding.** Praise precisely what is earned and why; name what is missing without detours; never move on while the student is approximate. "Almost" only when it is true.

## How it is implemented

- `backend/app/services/skill_professeur.py` — `SkillProfesseur` keeps three facts per session (a question is pending, number of attempts, turns) and returns the turn's instruction block `[GESTE DE PROF — ce tour]`, injected into the system prompt before the model speaks. The model declares its judgement of the student's answer at the start of its reply in `<eval>correct|partiel|faux|aucune</eval>`; the module reads it to count attempts, and `tag_decoder` strips the tag from chat, voice and history.
- Lesson phases (`lesson_phase.py`, `PHASE_RULES` in `llm_service.py`) say what the phase is for; the skill says what to do in this turn.
- Surfaces (scene, image, 3D, simulation, notebook) are chosen by `routeur_pedagogique.py`; explanation tactics per student by `teaching_tactics.py`; tone by `humanisation.py`.
- The animated professor (`frontend/src/services/professorEmotion.js`, `AIAvatar.tsx`, `Professor3D.tsx`) reacts to the tutor's words: greets, celebrates earned success, puts hands on heart, nods to encourage, laughs, is surprised; it points, writes on the board and operates simulations itself.

## When changing the teaching behaviour

- Change the rule in `skill_professeur.py` and its test `app/tests/test_skill_professeur.py` together; keep instructions imperative and short — a long instruction gets paraphrased instead of followed.
- Never make the model's judgement implicit: if a new state depends on what the student did, it must be declared in the reply (a tag) or measured from the conversation, never guessed.
- Run `python -m pytest app/tests/test_skill_professeur.py app/tests/test_tag_decoder.py app/tests/test_lesson_phase.py` from `backend`.
