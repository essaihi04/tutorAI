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

## 6. Spaced recall: from short-term to long-term memory (user rule, 11 November 2026)

- **One schedule per student and per competence**: after the course, each competence is due at J+1, then J+3, J+7, J+21, then before the exam (an interval ladder). A successful recall (right at the first try, no help) moves it one step up; a failed one moves it back to J+1; a hesitant one (right at the second try) stays on its step. A competence not acquired in the course starts at J+1 with the method recommended by `a_reprendre_avec`.
- **Same subject only**: the recall that opens a session draws only from competences of courses of the **same subject** as the course being opened (physique-chimie, SVT, mathématiques, each on its own). Never mix subjects.
- **3 minutes, 3–5 questions**, the most overdue first, from `competences[].rappels` (another wording than last time), without the course, without hints; then the session goes on. A free recall answer is judged live; a QCM one uses its prepared reaction.
- A recall counts as « retained » only when it is a first-try success after at least one day: that is what the J+7 and J+30 rates measure.

## 7. Traceability

Every event is recorded with its date and kept (JSONL per student today, the same place as the answers, `suivi_acquis.enregistrer`): course answers (as now), notebook written (block, time spent), retrieval of a block, exercise, recall (competence, step of the ladder, days since the last time, answer, verdict, time to answer), saturation detected (cause) and what the tutor did, session start/end and duration, notification sent / opened. From it, per student and per competence: the history (« trajet »), the next due date, the retention rate at J+7 / J+30. The admin dashboard shows the retention per course and per competence (what actually stays), and per student.

Code (11 November 2026): `backend/app/services/memoire_longue.py` (ladder, same-subject recalls, progression in the blocks, home-screen notification, retention), routes `backend/app/api/v1/endpoints/memoire.py` (`/course-player/memoire/seance/{deck}`, `/rappels/{matière}`, `/evenement`, `/accueil`, `/preferences`; the free link serves `seance` and `evenement` under `/public/cours-ondes/memoire/…`), admin `GET /admin/retention` (tab « Rétention », `AdminRetention.tsx`), tests `app/tests/test_memoire_longue.py`. These events carry `evenement` and `cours_id`, never `deck_id`, so a course's bilan only sees its answers. Player side: `frontend/src/components/course/memoire/` (`useMemoireDuCours` is wired in `CoursePlayer`; `CourseFocusStage` turns « Suite → » into « ✍️ Au cahier → » on the last slide of an unfinished block). Prepared reactions: `competences[].rappels[].reponses`, `seances[].blocs[].exercice.reponses` (vrai/faux: `statements[j].reponses`), each `{option: {juste|1|2: {parole, ecrit, audio}}}`; an exercise with `reprend: "<slide>/e<i>"` reads the slide's `concentration.reponses`.

## 8. Notifications, per student

- A notification only when something is due for THIS student: « 3 rappels de physique t'attendent (3 min) » — the subject, the number, the duration; never a generic reminder.
- At the student's usual study time (learned from his sessions), at most one per day, none when nothing is due; quieter after several ignored ones.
- The student chooses the time or turns them off in one tap; the notification opens straight on the recall, one tap away.
- Channels: in-app first (badge and banner on the home screen); web push or e-mail only where the platform already has them and the student agreed.

## 5. Rules of a good experience

- **The reprise cycle feeds the status** (professeur rule 22): each twin question is recorded as `cycle<n>` (1 try) with `methodes.reexplication = n`; a hand move away during a cycle is recorded as `cycle<n>_abandon`, wrong. So a competence left after a failed cycle, or abandoned, scores 0 on those items and comes out NOT ACQUIRED, with the reprise entries counted among the methods tried.
- **An answer given is final** (user rule, 8 November 2026): once a question is finished (right, or wrong twice after the hint), the student cannot answer it again — not by closing and reopening the board, not by coming back to the slide, not by reloading. The state of each question is kept per student, course, slide and question (`localStorage` key `reponse:<deck>:<slide>:<cle>`, and the events on the server), and restored on screen with its verdict. The only second chance is the one the teacher gives: one retry after the hint (professeur rule 3).
- Never block the student: recording is fire-and-forget; a failed call changes nothing on screen.
- Judge the notion, not the student: one wrong click is an attempt, the hint comes first (professeur rule 3); the status counts attempts, not time.
- A status moves only with evidence: `acquis` needs a first-try success; `partiel` says « revu avec aide » ; a gap leaves only through a new success on another question.
- Always pair a gap with a method: the point is not a red mark but « reprends-le avec la simulation que tu manipules toi-même ».
- Keep the labels in the bac's words, so the student recognises them in the exam instructions.
- Simple and pleasant first: recall, notebook and exercise steps add no menu and no new screen to learn; one main button; a failed recall is « on la revoit bientôt », never a red mark.
