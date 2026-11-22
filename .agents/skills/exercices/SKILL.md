---
name: exercices
description: How to create the exercises of the « Exercices » part (2ᵉ Bac PC BIOF, first semester, maths / physique-chimie / SVT) — original application exercises, never a national subject (those belong to the Examen part), never a copied paper; statement in JSON with its figures drawn in code, prepared tutor hints with voices, an animated explanation and an easier QCM / true-false / association version reusing the course player, a writing sheet, a keyboard per answer, and a similar exercise with other data that the tutor only corrects. Use whenever an exercise is created, reviewed, voiced or published, or when the user asks for exercises on a chapter; chains exploration-de-cours, cours-concentration, professeur, voix-du-cours, prononciation, simulations-au-tableau and cahier-de-l-eleve.
---

# Exercices (partie « Exercices »)

The user's request (22 November 2026): « créer une autre partie qui s'appelle exercice, qu'on va utiliser avec les mêmes skills de création de cours… pour les 3 matières du premier semestre ; commencer par un exercice pour chaque matière, après validation on va élargir ». Every rule of the courses applies (simplify, demonstrate every detail while staying simple, no mistake in a text or a voice). Model exercises: `frontend/public/media/exercices/phys_ex_ch1_corde_1.json`, `math_ex_ch1_continuite_1.json`, `svt_ex_ch1_levures_1.json` (sources: `scratchpad`-style Python generators, see § 8).

## 1. What an exercise is — and is not

- **An application exercise of ONE course of the first semester** (`backend/data/curriculum/programme_semestre1.json`), on notions the course has taught (professeur rule 27: nothing asked that was not taught). Field `cours` = the course deck it applies.
- **Never a national subject**, not even rewritten with other numbers: the national exercises are in the Examen part (`/exam`, `frontend/public/media/examens/`). A question may have the *type* of a national question (« décrire puis déduire », « calculer τ », « déterminer a pour que f soit continue »), with our own situation and data.
- **Never a copied paper**: no scan, no photo, no text copied from a book, a series or a site. The statement is written by us, as content: text + data + figures drawn in code (`FigureCahierData`, the notebook figure format: `courbe`, `schema`, `croquis`, `variations`). « N'oublie pas les schémas »: every figure the question needs is drawn, with its labels, values and arrows.
- **Inside the cadre**: same checks as the courses (`controler_cadre.py`, `a_ne_pas_dire`, `exclus_hors_programme` of the exploration file).

## 2. Research before writing (mandatory)

User rules (22/11/2026): « pourquoi ne pas chercher sur internet les exercices déjà présents pour ne pas sortir de ce qui est demandé » ; « vérifier dans les vidéos YouTube transcrites s'il y a des exercices faits par les 10 profs, et ensuite comparer avec les exercices des examens, pour créer des exercices de qualité avec différents niveaux facile, moyen et difficile ».

1. **The 10 teachers' videos** of the chapter (skill `exploration-de-cours`; file `backend/data/curriculum/exploration/<clé>.json`: `sources.video_exercices`, `comparaison.erreurs_des_profs`, `cas_types`, `pieges`, `verification.une_video_exercices_national`). List the exercises they solve, the steps they insist on, their mistakes (never copy a teacher's mistake).
2. **Existing series online** (Moroccan 2ᵉ Bac PC BIOF: teachers' series and corrected series — e.g. talamidi, moutamadris, alloschool, dyrassa): 5 or more exercises of the chapter, to know the classic situations, the usual data and the expected level. Read only; write ours.
3. **The national exams** of the chapter (`sources.examens`, `erreurs_examen`, `redaction_nationale` of the exploration file; `backend/data/exams/<mat>/<année>-<session>/exam.json`): which question types fall, how they are worded, where points are lost. The exercise trains exactly these gestures (one line per period with values for a SVT description; « interpréter géométriquement » after a limit; the unit on every result).
4. Write down in the generator's header which sources were compared (one line each).

## 3. Levels

`niveau`: `facile` (one relation, one step, data given directly), `moyen` (two steps, or a reading of a document / curve before the calculation), `difficile` (a reasoning in several steps at the level of the national, with a document to exploit). Start each chapter with one `facile` or `moyen`; add the others after the user's validation. Inside an exercise, the questions go from the simplest to the hardest.

## 4. The JSON (`frontend/public/media/exercices/<id>.json`, listed in `index.json`)

Id: `<mat>_ex_ch<N>_<clé>_<n>` (`phys_ex_ch1_corde_1`). Types: `frontend/src/components/exercice/types.ts`.

- Top: `id, type: "exercice", version, status, matiere (physique|mathematiques|svt), chapitre, cours, titre, niveau, duree_min, origine ("Exercice original écrit pour Moalim…"), competences[]`.
- `enonce`: `intro` (French, as on a sheet), `intro_dit` (voice), `figures[]`, `donnees[]` (one datum per line, with units), `questions[]`.
- Each question: `id` (« 1 », « 2-1 »), `texte`, `texte_dit`, `reponse`, `clavier`, `aides`, `correction`, `explication`, `facile`.
  - `reponse.type: "valeur"` — judged in the browser (`juger.ts`): the number after the last « = » or « ≈ », relative `tolerance` (0,03 by default for physics, 0,001 for exact maths), `unite` (missing unit → a note, not a fault), `attendu` = the full written answer. `"phrase"` — judged by the tutor (`/course-player/answer-reaction` with `attendu`), with a self-check fallback when the tutor is offline.
  - `clavier: {aides, pieges}` — the symbols and relations useful for THIS answer, and plausible traps (never the full answer). The floating course keyboard shows them (`ChampReponse` suggestions), and the writing sheet too.
  - `aides[]` — 2 hints (sometimes 3), from the track to the method, **never the answer**: aide 1 shows what to look at (« pendant t₁, le front est parti de S et arrivé en P : quelle distance ? »), aide 2 gives the method or the relation (« v = SP/t₁ »). Each one has `texte` (French, written) and `dit` (voice).
  - `correction: {lignes[{texte, mot}], parole}` — the answer as it must be written on the exam copy: question number first (« 1 : … »), relation, numerical application, result with unit, conclusion sentence; `mot` = the passage of `parole` where the line is written.
  - `explication` / `facile`: ids of slides in the two decks below.
- `explication.activities[0].slides[]` — **course-format slides** (skill `cours-concentration`): one per question, `visual.kind: "simulation"` with an EXISTING chalk simulation of the course (same `?vue=`, `play_until` on its named `moments`, `set_parameters`), `speech_text.mixed`, `concentration.centre` and `pointage` (each `mot` is a substring of the speech). The values the voice says must be those the simulation shows (read the simulation's constants first: corde.html `V = 1.0 m/s, θ = 0,4 s`; raccord.html `fa`; exao.html levures; rendement.html 38 × 30,5 / 2860). Realistic animation, as in the course: no new static picture when a simulation exists.
- `facile.activities[0].slides[]` — one slide per question, the same notion made easy: a `qcm` (`question.options`, `correct`, `enonce_dit`, `concentration.reponses.q.<i>.{juste | 1, 2}` — professeur rule 20: a prepared reaction for every option, the misconception named), a `vrai_faux` (`exercises[].statements` with `explanation`) or an `association` (professeur rule 47: `couples`, `retours` for every pair, `bilan`). A short `speech_text.mixed` introduces it.
- `similaire: {id, titre, enonce}` — **the same exercise with other data** (same questions, other numbers or another function / experiment, same difficulty), with `reponse`, `clavier` and `correction` only: no `aides`, no `facile`, no `explication`.

## 5. Voice texts (all `dit`, `parole`, `intro_dit`, `texte_dit`, `enonce_dit`, `mixed`, `mot`)

Skills `voix-du-cours` and `prononciation`, with the lessons learned on the courses:
- darija explains, French carries the terms, numbers, units, relations; **never a darija word next to a French number** (`texte_parle.nombres_darija_fr`: « تقريبا huit » → « environ huit », « جوج noyaux » → « deux noyaux »); every word fully in one alphabet; no digit, symbol or markdown; θ said « teta », ℓ said « L »; French sentences cut with commas;
- run the generator's final pass (`finir.py`: applies `nombres_darija_fr` to every voice field, checks every `mot` is in its speech and that no digit is spoken) before any generation;
- voice Bodi, **batch WITHOUT tunnel only** (`/srv/corpus_v4/voix_lot/lancer_lot.sh N pousser`, list `[{cle, texte, cours}]` with `cle = "<id_exercice>/<dossier>/<piste>"`), then **transcription check of every track**: the numbers heard must be the numbers written (word-by-word alignment, a darija number in place of a French one = regenerate).
- Tracks: `frontend/public/media/audio/exercices/<id>/<dossier>/<piste>_v<V>.mp3`; fields `intro_audio`, `texte_audio`, `aides[].audio`, `correction.audio`, and in the slides the course fields (`audio.mixed`, `reponses…audio`, `enonce_audio`, `retours…audio`).

## 6. The student's screen (built: `frontend/src/pages/ExercicePage.tsx`, list `ExercicesHub.tsx`, route `/exercices/:id`)

The statement on the left (text, figures, data, listenable), one question at a time on the right with: the answer field and its keyboard; « 🙋 Aide du tuteur » (hints one by one, with their voice); « 🎬 Explication animée » (the explanation slide in the course player, starting at once); « 🎯 Plus facile, pour s'entraîner » (the easy slide); « Voir la correction » after a try; « 📝 Ma feuille » (lined sheet where the student writes the whole answer, symbols of the question, full keyboard on demand, photo of his paper; kept in the browser). At the end, a review and the « 🔁 Exercice semblable », put forward when he made mistakes, asked every hint or watched an explanation.

## 7. Checks before showing the user

1. JSON valid; every question has `reponse`, `clavier`, `correction`; every `explication` / `facile` id exists; `similaire` has the same number of questions.
2. Numerical answers recomputed (by hand or in Python) and judged by `juger.ts` with the expected writing (`v = SP/t₁ = 0,6/0,6 = 1 m/s` → juste).
3. `finir.py` prints « problèmes : 0 ».
4. `npx tsc --noEmit` passes; the three screens open in the browser (statement, figure, a wrong answer, a hint, the right answer and its correction, the explanation playing its simulation, the easy version, the sheet).
5. Voices generated, transcribed and placed; no slide or hint without its track.

## 8. Generators

Each exercise is written as a small Python generator (`<id>.py`) that builds the JSON (helpers `qcm_facile`, `rep`, figure functions), so that a datum changed once changes everywhere; then `finir.py <texte_parle.py> out/*.json`, then copy to `frontend/public/media/exercices/` and rebuild `index.json`.
