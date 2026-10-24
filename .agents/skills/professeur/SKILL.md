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
4. **Unclear answer: ask once, then judge.** An answer that cannot be judged (ambiguous, cut off, badly transcribed) is neither right nor wrong: the tutor asks the student to clarify, with no hint and no attempt counted. Only once; on the next turn it must judge.
5. **Re-read what must be learnt word for word.** At the end of an explanation block, the tutor re-reads the one key sentence (definition, or formula with the meaning of each term), announced by "Je relis :", exactly as on the board. When the student asks to hear it again ("répète", "عاود", "ما سمعتش"), the tutor re-reads it identically and adds nothing; this is not an attempt. "Je ne comprends pas" is different: change the angle. "se répète" is a physics answer, not a request.
6. **Read a problem statement twice before any calculation.** First reading: "what is this exercise about?" in one sentence. Second, active reading: the data with their units, what is asked, and the verb of the instruction (calculer, justifier, montrer que, déduire). Neither reading is graded (`<eval>aucune</eval>`); solving starts after.
7. **Prerequisite gap: open a parenthesis, then come back.** When the error comes from a competency of earlier years (TC, 1re bac, collège — e.g. derivatives, projecting a vector, cell structure), the tutor says "On ouvre une parenthèse : [titre]", re-explains it in 3 to 5 sentences with an example from the original level, re-reads the key sentence, asks one verification question, then says "On ferme la parenthèse" and re-asks the course question unchanged, with fresh attempts. Never nested, at most 3 per session. The candidate prerequisites per chapter live in `backend/data/curriculum/prerequis.json` (each with its official source) and are offered to the model only after a first failed attempt; the model declares one with `<prerequis>id</prerequis>`, ids outside the chapter's list are ignored. Opening/closing is sent to the screen (`parenthese` event) and the closing is recorded in `student_answer_history` with `source = "parenthese"`.
8. **Warm and demanding.** Praise precisely what is earned and why; name what is missing without detours; never move on while the student is approximate. "Almost" only when it is true.

## How it is implemented

- `backend/app/services/skill_professeur.py` — `SkillProfesseur` keeps three facts per session (a question is pending, number of attempts, turns) and returns the turn's instruction block `[GESTE DE PROF — ce tour]`, injected into the system prompt before the model speaks. The model declares its judgement of the student's answer at the start of its reply in `<eval>correct|partiel|faux|incertain|aucune</eval>`; the module reads it to count attempts (`incertain`: the answer cannot be judged, so the tutor asks once for clarification without counting an attempt), and `tag_decoder` strips the tag from chat, voice and history.
- Lesson phases (`lesson_phase.py`, `PHASE_RULES` in `llm_service.py`) say what the phase is for; the skill says what to do in this turn.
- Surfaces (scene, image, 3D, simulation, notebook) are chosen by `routeur_pedagogique.py`; explanation tactics per student by `teaching_tactics.py`; tone by `humanisation.py`.
- The animated professor (`frontend/src/services/professorEmotion.js`, `AIAvatar.tsx`, `Professor3D.tsx`) reacts to the tutor's words: greets, celebrates earned success, puts hands on heart, nods to encourage, laughs, is surprised; it points, writes on the board and operates simulations itself.

## When changing the teaching behaviour

- Change the rule in `skill_professeur.py` and its test `app/tests/test_skill_professeur.py` together; keep instructions imperative and short — a long instruction gets paraphrased instead of followed.
- Never make the model's judgement implicit: if a new state depends on what the student did, it must be declared in the reply (a tag) or measured from the conversation, never guessed.
- Run `python -m pytest app/tests/test_skill_professeur.py app/tests/test_tag_decoder.py app/tests/test_lesson_phase.py` from `backend`.
