---
name: suivi-des-acquis
description: How the platform follows what each student has acquired, partly acquired or not acquired, competence by competence, from their answers to the course questions — together with the explanation method that worked or failed for them — and how the free mode and the next courses reuse these gaps. Use whenever a course is cut into competences, a question is written or keyed, an answer is recorded, a student's gaps or progress are asked for, the free-mode tutor adapts to a student, or a remediation is planned.
---

# Suivi des acquis, par compétence

User rule, 8 November 2026: every course is cut into **competences**, each question is attached to one, every answer is recorded with the way the notion was explained, and the result (acquis / partiel / non acquis, with the methods that work for THIS student) feeds the free mode and the next courses. Code: `backend/app/services/suivi_acquis.py`, endpoint `/course-player/acquis` (POST an answer, GET `/acquis/{deck_id}` the bilan), tests `app/tests/test_suivi_acquis.py`.

## 1. Cut the course into competences (when building it — skill `cours-concentration`, step 1)

- `deck.competences = [{id, label, slide_ids}]`: 6 to 10 per chapter, each one a verb the bac uses (reconnaître, distinguer, calculer, utiliser, relier, lire, mesurer, exploiter, rédiger) + the notion. Example (waves): C1 reconnaître une onde mécanique progressive… C9 rédiger comme le barème.
- Each slide carries `competence_ids` (usually one). A question or exercise belongs to its slide's competence.
- Every question has its key (`question.correct`, exercises `correct`): without a key nothing can be judged.

## 2. What is recorded, at every answer (`CourseFocusStage.enregistrerReponse`)

`{deck_id, slide_id, cle, type (qcm | vrai_faux | directe), enonce, reponse, tentative, correct, reaction_preparee, methodes}` where `methodes` says how the notion had just been explained: `visuel` (simulation | image | table | schema | aucun), `formules_au_centre`, `tuteur_a_montre`, `eleve_a_manipule`, `variante_du_tuteur`, `exercice`. A free answer judged by DeepSeek is recorded with its verdict; an unjudgeable one with `correct: null`.

Storage today: one JSONL per student in `backend/data/suivi_acquis/` (no table before the user validates; `enregistrer` is the single place to switch to Supabase later, next to `student_answer_history`).

## 3. How it is judged (`bilan`)

- Per question: **1** right at the first try, **0,5** right at the second, **0** never right, none if nothing judgeable. Per competence: the mean → **acquis ≥ 0,8**, **partiel ≥ 0,4**, **non acquis** below, **non évalué** without answers.
- **Trajet**: for each competence, the ordered list « diapositive : statut (méthodes) » — what was tried.
- **Methods that work**: success rate per method label (simulation, image, table, formules, tuteur_montre, eleve_manipule, variante, exercice, question_cours, qcm, vrai_faux, directe) over all this student's answers; `methodes_qui_marchent` = those ≥ 0,8.
- For each gap: `methodes_qui_ont_echoue` (the methods of its failed questions) and `a_reprendre_avec` = the student's best-working methods that are not among the failed ones; failing that, manipulated simulation, then exercise.

## 4. How it is reused

- **Free mode**: `session_handler._bloc_acquis()` puts `[ACQUIS DE L'ÉLÈVE — <cours>]` at the top of the system prompt: what is acquired (lean on it, do not re-explain), each gap with the method that failed and the one to use instead, one question on it when the occasion comes, and the Duolingo rule of the error box (`boite_erreurs`): a notion is reconquered only by a NEW success, later, not by rereading or the twin question.
- **Next course / remediation**: `lacunes(bilan)` lists the competences to rework with `reprendre_avec` and the trajet. When a new course of the same subject is built (skill `cours-concentration`), its first slide revisits these gaps **with the recommended method** (a manipulated simulation and an exercise rather than another image), and its questions re-ask them so the status can change.
- **Teacher / student view** (to build): GET `/course-player/acquis/{deck_id}` already returns the full bilan, the lacunes and the prompt block.

## 5. Rules of a good experience

- **The reprise cycle feeds the status** (professeur rule 22): each twin question is recorded as `cycle<n>` (1 try) with `methodes.reexplication = n`; a hand move away during a cycle is recorded as `cycle<n>_abandon`, wrong. So a competence left after a failed cycle, or abandoned, scores 0 on those items and comes out NOT ACQUIRED, with the reprise entries counted among the methods tried.
- **An answer given is final** (user rule, 8 November 2026): once a question is finished (right, or wrong twice after the hint), the student cannot answer it again — not by closing and reopening the board, not by coming back to the slide, not by reloading. The state of each question is kept per student, course, slide and question (`localStorage` key `reponse:<deck>:<slide>:<cle>`, and the events on the server), and restored on screen with its verdict. The only second chance is the one the teacher gives: one retry after the hint (professeur rule 3).
- Never block the student: recording is fire-and-forget; a failed call changes nothing on screen.
- Judge the notion, not the student: one wrong click is an attempt, the hint comes first (professeur rule 3); the status counts attempts, not time.
- A status moves only with evidence: `acquis` needs a first-try success; `partiel` says « revu avec aide » ; a gap leaves only through a new success on another question.
- Always pair a gap with a method: the point is not a red mark but « reprends-le avec la simulation que tu manipules toi-même ».
- Keep the labels in the bac's words, so the student recognises them in the exam instructions.
