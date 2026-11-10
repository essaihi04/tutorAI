---
name: voix-du-cours
description: How to write the spoken darija text of a course (speech_text.mixed) so the Moalim voice says it correctly and trains the student for French exams, then generate it on Kaggle with the latest checkpoint, check it by transcription and place it in the course. Use for any course voice track, any change to what the voice reads, or a new course to voice; for the tutor's live replies see llm_service.py rules and the professeur skill.
---

# Voix du cours

The voice is a Chatterbox model fine-tuned on Moroccan teachers (v4, kernel `ferdaous04/academy-v4-entrainement`, file `t3_mtl23ls_v2.safetensors`, Amine's « vif » reference). It says well what it heard in training and badly what it never heard. The student must understand the darija AND learn the French he will write in tests and at the national exam. Rules validated by the user, 7 November 2026, on the waves example course.

## 1. Write the text

**Darija carries the explanation; French carries everything the student will write.**

- **French, always:**
  - the programme's technical terms (l'onde, la perturbation, la célérité, le retard, le front, l'élongation, l'aspect, la source, le milieu, transversale, longitudinale, la sensibilité, la division, l'oscilloscope…);
  - **numbers**, as BIOF teachers say them: deux, zéro virgule deux, trois cent quarante, mille cinq cents, deux fois dix puissance moins trois;
  - **units, always in French words, never the symbol and never in darija** (not « متر فالثانية », not « ميلي ثانية »): m/s → mètre par seconde, km/h → kilomètre par heure, s → seconde, ms → milliseconde, µs → microseconde, min → minute, h → heure, m → mètre, cm → centimètre, mm → millimètre, km → kilomètre, Hz → hertz, kHz → kilohertz, N → newton, J → joule, W → watt, V → volt, A → ampère, Ω → ohm, F → farad, °C → degré Celsius, K → kelvin, kg → kilogramme, g → gramme, mol → mole, mol/L → mole par litre, L → litre, Pa → pascal. A value is said with its unit: « trois cent quarante mètres par seconde », « quarante millisecondes », « zéro virgule cinq milliseconde par division »; the conversion too: « deux millisecondes égale deux fois dix puissance moins trois seconde »;
  - **no audible plural S.** In French the final s (or x) of a plural is silent, but the voice reads it when it has rarely heard the plural form: « les micros » came out « micross ». The text keeps correct French; the generator passes it through `corpus_v4/pluriels_muets.py`, which writes each French plural seen fewer than 50 times in the corpus in its singular spelling (« les micro », « les division »), so it is said as a teacher says it. Words whose final s is pronounced (plus, sens, bus, virus, hélas, os…) and plurals the corpus knows well (les, électrons, mètres…) are left alone;
  - **equations and operations**, said entirely in French: « v égale d sur delta t », « tau égale SM sur v », « L égale v fois teta », « deux d égale v fois tau, donc d égale v fois tau sur deux », « y de M de t égale y de S de t moins tau ». The words are plus, moins, fois, sur (or divisé par), égale, puissance, au carré, racine carrée, delta;
  - **« en fonction de »** for every graph or relation: « y en fonction de t », « y en fonction de x », « delta t en fonction de d »;
  - **the exam words**, so the student hears them before reading them in a test: calculer, déterminer, déduire, justifier, montrer que, représenter, l'expression, la relation, l'application numérique, la valeur, le résultat, vrai, faux;
  - the simple French words every student already uses: donc, alors, voilà, d'accord, c'est, bien, déjà.
- **Simple darija for everything else.** A French word that is none of the above (« la bouée », « la queue », « la manip », « clap », « impulsion », « le barème », « l'énoncé », « le trajet ») was never heard by the voice and many students do not know it: say it in everyday darija (« واحد الكورة صغيرة فوق الما », « اللخر ديال la perturbation », « فالتجربة », « كنضرب بيدي », « السؤال »).
- **Common darija, short sentences.** One idea per sentence, verb near the start. Prefer the words teachers use most in the corpus: يعني، دابا، إذن، هادي، شنو، كيفاش، علاش، واش، باش، شحال، مثلا، مزيان، بحال، ملي، **يلا** (not « إلا »). Avoid rare or literary words and long glued forms (« فالمراية », « مزحزحين », « كتحسم », « وكيبعدو » never occur in the corpus).
- **No tashkil, ever.** The corpus has none; harakat push the model off its training and make the word worse. A word that seems to need vowels is replaced by a simpler one (or said in French if it is a programme term).
- **Symbols as the corpus writes them:** teta (not thêta), tau, delta t, lambda, y. Letters for points as they are: S, M, A.
- **Definitions to learn by heart** are re-read in French, word for word, after « نعاود نقرا : » (professeur skill, rule 5). **Cut every French sentence longer than about ten words with commas** (« le point M reproduit le mouvement de la source, avec un retard tau, égal à SM sur v »): the generator makes one piece per comma group, and a long all-French piece is where the darija-trained voice loses its way.
- **No symbols, no digits, no markdown** in the text: everything is written as it is said (`texte_parle.py` turns what is left into words, but the text should not rely on it).

## 2. Check every word against the training corpus

```bash
python C:/Users/HP/Desktop/voxtts/corpus_v4/verifier_texte_corpus.py <cours.json>
```

It reads every `speech_text.mixed`, applies `texte_parle.py`, and lists French words seen fewer than 20 times that are not programme or exam words, and darija words seen fewer than 3 times. Replace them with corpus words (look a candidate up the same way before using it) until the list is empty or only holds words you keep on purpose (a programme term the student must hear for the bac, said with its article and explained once in darija). The corpus file is `corpus_v4/selection_train.jsonl` (dataset `zouhairessaihi/academy-v4-selection`, 38 852 sentences, 28 % French words).

Measured on the waves example: rewriting with these rules raised the words recognised by transcription from 67 % to 78 % on average, and the worst slide from 50 % to 69 %.

## 3. Generate on Kaggle with the latest checkpoint

**The course voice is Bodi** (user rule, 10 November 2026): every slide track and every prepared reaction is generated with the most recent model, `academy-v5-bodi` (the backend's `kaggle_tts_modele` on the VPS), never with the Amine reference of `gen_kaggle_cours_exemple.py`. Route: a script on the VPS, run from `/opt/moalim/backend` with `/etc/moalim/backend.env` loaded, wakes the test kernel (`scripts.kaggle_tts._reveiller_essai`) and posts each text to `/tts` (`{"texte", "langue": "ma", "pas_flow": 10}`), two at a time (one per T4); models: `/srv/corpus_v4/cours_bodi/voix_bodi.py` (waves course) and `/srv/corpus_v4/cours_op_bodi/voix_bodi_op.py` (periodic waves: writes `mixed/<id>.wav`, `reponses/<id>.wav` and a `cours.json` of `{id, hash}` per folder, so `poser_pistes_exemple.py <dir> <version> <cours>` and `preparer_reponses.py audio` place them). The account has only **two GPU sessions**: a kernel already running keeps its session until it ends, even if a new version is pushed over it (the status shows only the newest version); « Maximum batch GPU session count of 2 reached » then makes the wake-up read an old log with a dead tunnel — wait for the slot (`cours_op_bodi/attendre.sh` retries every 10 min).

The steps below are the older Amine route, kept for reference.

- The weights are on the **ferdaous04** account; its credentials are only on the VPS (`/etc/moalim/backend.env`). The local Kaggle CLI is logged in as zouhairessaihi and cannot read ferdaous04's private kernels. So the kernel is built locally and **pushed from the VPS**:
  1. `python C:/Users/HP/Desktop/voxtts/gen_kaggle_cours_exemple.py` builds `corpus_v4/kernel_cours_exemple/` (v8 recipe: spoken-text rules, pauses after « : » and « ; », Amine vif reference, `kernel_sources: ferdaous04/academy-v4-entrainement`). For another course, change the course file it reads and the kernel id.
  2. `scp` the folder to the VPS, then `set -a; . /etc/moalim/backend.env; set +a; HOME=/tmp/kh /opt/moalim/backend/.venv/bin/kaggle kernels push -p <folder>` (never print the env).
  3. Wait with `kaggle kernels status` (about 15–20 min for 15 slides on a T4), then `kaggle kernels output … -p <dir>`; the log line « modèle /kaggle/input/…/ferdaous04/academy-v4-entrainement/… » proves which weights were used.
  4. Clean the temporary folders on the VPS afterwards.
- **Never push `academy-tts-direct` by hand** (the live voice kernel): use a separate kernel id.

## 4. Check what the voice actually says

- Audio sanity: no clipping, longest silence under 2 s, and **no mumble**: `python C:/Users/HP/Desktop/voxtts/corpus_v4/detecter_murmures.py <dossier des wav>` must print only `ok`. A mumble is the voice dropping out mid-sentence: one second or more of low, dull sound (between -52 and -30 dB, neither speech nor silence) before the voice comes back. The student hears a small noise, then nothing, then the voice again. Met on 8 November 2026 in `wx_r1_retard_v4.wav` (40,2 → 43,6 s): the long all-French re-read « … avec un retard tau égal à SM sur v » came out as « T ممم تا ممها ». The transcription shows it too (« ممم », words missing at the end of a French sentence). Regenerate that slide with another seed after cutting the sentence with commas; never place a track that still has a mumble.
- Transcription with MoulSot (`atlasia/moulsot.v0.3`, darija ASR) on Kaggle: `corpus_v4/kaggle_verif_moulsot.py` (kernel source = the generation kernel), cut at silences into ≤ 20 s pieces. Compare the Arabic words of the spoken text with the transcription, slide by slide; list the passages of 3 or more words that are missing. MoulSot hears French badly and writes numbers as digits, so a low score is a pointer for listening, not a verdict.
- Give the user a **listening page** (track, text, transcription, score, « Bien / À refaire ») and redo only the slides they mark.

## 5. Same rules for the tutor's live replies (free questions)

The live voice (`backend/kaggle_tts/serveur.py`, kernel `academy-tts-direct`) uses the same model, so it fails the same way:
- the prompt ([RÈGLE DE SÉCURITÉ — PRONONCIATION ET FRANÇAIS] in `llm_service.py`) tells the model to cut every all-French sentence longer than ten words with commas;
- each piece is checked with `murmure()` as soon as it is generated; a piece that mumbles is generated once more before it is sent (log line « murmure, morceau refait »). The test is `test_un_morceau_qui_murmure_est_refait` in `app/tests/test_kaggle_tts.py`;
- the course generator (`gen_kaggle_cours_exemple.py`) does the same with up to 3 new seeds, and `seules=<id,id>` regenerates only the listed slides.
- the tutor's PREPARED reactions to every possible answer (professeur skill, rule 20) are voiced by the same generator: `python gen_kaggle_cours_exemple.py reponses=<pistes.json>` (a list of `{id, parole}`, kernel `ferdaous04/academy-cours-reponses`); the `parole` texts follow the rules of section 1 (they are written by DeepSeek with these rules in its prompt, then checked: no digits, no symbols). Tracks go to `/media/audio/courses/<deck>/reponses/<id>_v<N>.wav` and their url into the reaction (`audio`).

## 6. Place the tracks in the course

`corpus_v4/poser_pistes_exemple.py <output dir> <version>` copies each `<slide id>.wav` only if its text hash matches the current `speech_text.mixed`, and writes `slide.audio.mixed = {url, duration_ms, version, speech_hash, status}`. Bump the version in the file name (`_v3.wav`, …) at each regeneration so browsers do not replay a cached old track, and delete the previous files.
