---
name: tuteur-exercices
description: How the tutor uses the exercises of the « Exercices » part with a student — when to propose one, how to help without giving the answer (prepared hints first), when to show the animated explanation or the easier QCM / true-false / association version, how to correct a written answer, and when to give the similar exercise with other data that the tutor only corrects. Use when changing the exercise screen, the tutor's behaviour around exercises, the student profile's « à faire », or when a student asks for help on an exercise.
---

# Le tuteur et les exercices

User's request (22 November 2026): « si l'élève veut avoir de l'aide de notre tuteur, ici on va préparer l'audio et les aides disponibles pour cet exercice ; il demande aussi explication, donc on va expliquer l'exercice avec des animations réalistes comme dans le cours ; … au cas où l'élève demande tout au tuteur, il n'a rien fait, ou plus de fautes, donner une autre exercice similaire avec des données différentes, mais cette fois seulement avec explication, sans aide de correction : il va juste corriger ; … le premier exercice, vous pouvez le donner sous forme de QCM, association, vrai/faux s'il le trouve difficile, pour s'entraîner ». Content contract: skill `exercices`.

## 1. When the tutor proposes an exercise

- After a course block or a course: the exercises whose `cours` is that course, in order of level: `facile` (to train), then `moyen` (the level of the national), then `difficile` (« Supérieur », above the national, same form). Move to the next level when the similar exercise of the current one is right alone.
- From the student profile (`/course-player/profil`, `a_faire` items `type: "exercice"`): a competence not acquired or partial → the exercise of its chapter.
- In free mode (« تمرين », « exercice »): the tutor opens `/exercices/<id>` of the chapter being studied. Never a national subject here: for those, the Examen part.

## 2. During the exercise: the student leads, the tutor answers what he asks

The student first tries alone. The tutor never volunteers the answer. In order of what the student asks:
1. **« Aide du tuteur »**: the prepared hints, one at a time, with their voice (`aides[k].dit` / `audio`): aide 1 = what to look at, aide 2 = the method or the relation. No live generation, no waiting.
2. **A wrong answer**: first try → « pas encore », and the student may ask a hint; second wrong try → the correction (written lines + voice). A numerical answer is judged at once in the browser; a written answer goes to the tutor (`answer-reaction`, `attendu` given): right → what is right and why; wrong at the first try → one targeted hint; at the second → the answer and its justification.
3. **« Explication animée »**: the course-style slide of that question, with the course's own simulation and the 3D tutor (same gestures: `play_until`, `centre`, `pointage`). Realistic, simple, every step shown.
4. **« Plus facile, pour s'entraîner »**: the same notion as a QCM, true/false or association, a prepared reaction for every answer; then back to the real question.
5. **« Voir la correction »**: the expected writing for the exam copy (question number, relation, numerical application, result with unit, conclusion).
6. **« Ma feuille »**: the student writes his full answer (keyboard with the question's symbols, photo of his paper).

## 3. After the exercise: the similar exercise

When every question is done, the review shows the score and the hints used. The tutor proposes the **similar exercise** (`similaire`: same questions, other data), and puts it forward when the student made at least one mistake, asked all the hints, did nothing alone, or watched an explanation. In the similar exercise:
- no hint, no easy version, no animated explanation: the student works alone;
- each answer is **only corrected**: right or wrong, then the correction (the tutor's `answer-reaction` with the last attempt, which gives the answer and its justification at once);
- at the end, the review: all right → « la méthode est acquise » (competence acquired); otherwise → reread the corrections, then redo the missed questions.

## 4. Tone and voice

Same as the courses (professeur skill): warm, never a reproach, never congratulating a wrong answer, short sentences, darija + French with the voice rules (`voix-du-cours`, numbers never mixed). All prepared voices come from the batch without tunnel and are checked by transcription.

## 5. What is recorded, and the progression (built 22 November 2026)

User request: « câbler les résultats des cours avec les résultats des exercices pour donner une note à chaque cours et matière, suivre la progression, savoir ses lacunes et ses points forts ».
- Each marked answer (last attempt of a question, exercise or similar mode) is POSTed by `ExercicePage` to `/api/v1/exercices/resultat`: exercise, course, subject, level, question, attempt, note / sur, right, partial, hints used, explanation / easy version watched, points lost (`pertes`). Stored per student in `backend/data/resultats_exercices/<id>.jsonl` (`services/resultats_exercices.py`); also kept in the browser (`moalim:exercices:progres`) when offline.
- `/api/v1/exercices/progression` crosses them with the course results (competences of `suivi_acquis` through `stats_cours.tableau`): per exercise (note, questions done, status à faire / en cours / réussi ≥ 75 % / à revoir < 50 %, « acquis » when the similar exercise is right alone), per course (course % = acquired + ½ partial competences; exercises % = points obtained / points; course note /20 = 60 % exercises + 40 % course when both exist), per subject (mean of its courses), strengths (≥ 75 %), gaps (< 50 %, with the course's non-acquired competences) and the most frequent points lost.
- The list page (`ExercicesHub`) shows them: general note and one ring per subject, strengths / gaps / « où je perds des points », filters (subject, course with its note, difficulty, status, search), cards with the figure as thumbnail, difficulty bars, progress bar and note.
- Next: feed `profil_eleve` (`a_faire`) and the free-mode tutor with these exercise gaps, and the J+7 memory with the similar exercises done alone.
