# Test MULTI-TOURS — COACHING — switch exam / genes liés / tableau

_Généré le 2026-05-01 18:34:24_


**Contexte coaching :** `SVT` — Génétique humaine — transmission de deux gènes / Brassage interchromosomique — dihybridisme.


## Score : **7/7** — 🎉 TOUT VERT


| # | Tour | Path | Action | Subject ouverte | exam_id | Verdict |
|---|---|---|---|---|---|---|
| 1 | T1 — coaching : demander un premier exercice BAC | `primary_ok` | `open` | `SVT` | `svt_2025_rattrapage` | ✅ |
| 2 | T2 — coaching : un AUTRE exercice BAC (switch #1) | `primary_ok` | `open` | `SVT` | `svt_2019_rattrapage` | ✅ |
| 3 | T3 — coaching : encore un AUTRE (switch #2) | `primary_ok` | `open` | `SVT` | `svt_2025_rattrapage` | ✅ |
| 4 | T4 — coaching : BUG — génétique DEUX GÈNES LIÉS | `primary_ok` | `open` | `SVT` | `svt_2024_rattrapage` | ✅ |
| 5 | T5 — coaching : explication au TABLEAU (pas d'exam) | `no_action` | `stay` | `—` | `—` | ✅ |
| 6 | T6 — coaching : BUG — après tableau, ré-ouvrir un exame | `primary_ok` | `open` | `SVT` | `svt_2025_rattrapage` | ✅ |
| 7 | T7 — coaching : verrou matière (doit rester SVT) | `primary_ok` | `open` | `SVT` | `svt_2022_rattrapage` | ✅ |

---

## 1. T1 — coaching : demander un premier exercice BAC

**Message utilisateur :**
> Avant de continuer la leçon, peux-tu m'ouvrir un exercice BAC SVT pour pratiquer le dihybridisme (croisement F1×F1, échiquier) ? Un vrai exercice BAC officiel.

**État AVANT ce tour :**
```json
null
```

**Tag `<exam_exercise>` émis** : `dihybridisme croisement F1 F1 échiquier génétique`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `primary: tag='dihybridisme croisement F1 F1 échiquier génétique'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (203 chars — extrait) :**
```
Très bien ! Je vais te chercher un exercice BAC officiel sur le dihybridisme. Attends une seconde, je lance la recherche.

<exam_exercise>dihybridisme croisement F1 F1 échiquier génétique</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

---

## 2. T2 — coaching : un AUTRE exercice BAC (switch #1)

**Message utilisateur :**
> Merci ! Ferme celui-ci et ouvre-moi un AUTRE exercice BAC SVT sur la génétique (monohybridisme ou dihybridisme, peu importe).

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

**Tag `<exam_exercise>` émis** : `génétique monohybridisme dihybridisme croisement`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2019 Rattrapage** — _Exercice 2 | A partir des résultats du croisement 1 et 2, donnez les génotypes probables des chiens normaux et des chiens hairless, j_ (matière : **SVT**)
- log backend :
  - `primary: tag='génétique monohybridisme dihybridisme croisement'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (180 chars — extrait) :**
```
D'accord, je ferme l'exercice actuel et je t'ouvre un autre exercice BAC officiel sur la génétique.

<exam_exercise>génétique monohybridisme dihybridisme croisement</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2019_rattrapage",
  "subject": "SVT",
  "year": 2019,
  "session": "Rattrapage",
  "exam_title": "SVT 2019 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 4,
  "question_content": "A partir des résultats du croisement 1 et 2, donnez les génotypes probables des chiens normaux et des chiens hairless, justifiez votre réponse."
}
```

---

## 3. T3 — coaching : encore un AUTRE (switch #2)

**Message utilisateur :**
> Super. Ferme et ouvre un AUTRE exercice BAC SVT, année différente si possible, sur le même thème génétique.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2019_rattrapage",
  "subject": "SVT",
  "year": 2019,
  "session": "Rattrapage",
  "exam_title": "SVT 2019 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 4,
  "question_content": "A partir des résultats du croisement 1 et 2, donnez les génotypes probables des chiens normaux et des chiens hairless, justifiez votre réponse."
}
```

**Tag `<exam_exercise>` émis** : `génétique croisement dihybridisme monohybridisme BAC SVT`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `primary: tag='génétique croisement dihybridisme monohybridisme BAC SVT'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (194 chars — extrait) :**
```
D'accord, je ferme tout et je t'ouvre un autre exercice BAC officiel, année différente, sur la génétique.

<exam_exercise>génétique croisement dihybridisme monohybridisme BAC SVT</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

---

## 4. T4 — coaching : BUG — génétique DEUX GÈNES LIÉS

**Message utilisateur :**
> Maintenant je veux un exercice BAC SVT sur deux GÈNES LIÉS (linkage, brassage intrachromosomique, test-cross). Ferme l'exercice actuel et ouvre le nouveau.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

**Tag `<exam_exercise>` émis** : `gènes liés linkage brassage intrachromosomique test-cross BAC SVT`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2024 Rattrapage** — _Exercice 2 | En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis _ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés linkage brassage intrachromosomique test-cross BAC SVT'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 2 | En se basant sur les données du document 1, décrire le mode d'actio' ne contient aucun de ['lie', 'linkage', 'intrachromos', 'brassage', 'hybrid'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (255 chars — extrait) :**
```
Parfait ! Je ferme l'exercice actuel et je lance la recherche d'un exercice BAC officiel sur les gènes liés, le brassage intrachromosomique et le test-cross.

<exam_exercise>gènes liés linkage brassage intrachromosomique test-cross BAC SVT</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2024_rattrapage",
  "subject": "SVT",
  "year": 2024,
  "session": "Rattrapage",
  "exam_title": "SVT 2024 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 3,
  "question_content": "En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis montrer la relation entre le taux plasmatique de la progranuline et l'état de santé de la personne."
}
```

---

## 5. T5 — coaching : explication au TABLEAU (pas d'exam)

**Message utilisateur :**
> OK. Avant, explique-moi au TABLEAU la méthode pour résoudre un croisement avec deux gènes liés (test-cross, parentaux, recombinants, distance génétique).

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2024_rattrapage",
  "subject": "SVT",
  "year": 2024,
  "session": "Rattrapage",
  "exam_title": "SVT 2024 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 3,
  "question_content": "En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis montrer la relation entre le taux plasmatique de la progranuline et l'état de santé de la personne."
}
```

**Tag `<exam_exercise>` émis** : `(aucun)`

**Simulation backend :**
- subject_hint = `None` (subject_from_user=False)
- path_taken = `no_action`
- panel_action = `stay`
- log backend :
  - `AI emitted <ui> show_board (whiteboard)`
  - `no_tag_no_force: panel stays as-is`

**Checks :**
- ✅ PASS

**Réponse LLM (2027 chars — extrait) :**
```
واخا خويا! دابا غادي نشرح ليك la méthode كاملة على السبورة. هاد النوع ديال التمارين كاين فـ BAC 2022 normale و 2023 rattrapage. ركز معايا!

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Méthode : 2 gènes liés (test-cross)","lines":[
  {"type":"subtitle","content":"📖 Définition","color":"blue"},
  {"type":"box","content":"Deux gènes sont liés s'ils sont portés par la même paire de chromosomes homologues. Ils ne se séparent pas librement lors de la méiose.","color":"blue"},
  {"type":"subtitle","content":"🧭 Méthode en 4 étapes","color":"purple"},
  {"type":"step","content":"Identifier les phénotypes parentaux (P) et ceux du test-cross (F1 × double récessif)","label":"1","color":"blue"},
  {"type":"step","content":"Déterminer les 4 phénotypes de la descendance : 2 majoritaires (parentaux) + 2 minoritaires (recombinés)","label":"2","color":"blue"},
  {"type":"step","content":"Calculer le taux de recombinaison : d = (nombre de recombinés / total) × 100 (en %)","label":"3","color":"orange"},
  {"type":"math","content":"d = \\frac{R_1 + R_2}{\\text{Total}} \\times 100 \\quad (\\text{en \\% ou cM})"},
  {"type":"step","content":"Conclure : si d < 50 % → gènes liés. d = distance génétique en cM.","label":"4","color":"green"},
  {"type":"subtitle","content":"💡 Astuce BAC","color":"purple"},
  {"type":"note","content":"Les parentaux sont les plus nombreux. Les recombinés sont les moins nombreux.","color":"purple"},
  {"type":"subtitle","content":"⚠️ Piège classique (BAC 2021)","color":"orange"},
  {"type":"note","content":"Ne confonds pas gènes liés (même chromosome) et gènes indépendants (chromosomes différents). Si d = 50 % → indépendants !","color":"orange"},
  {"type":"subtitle","content":"📝 À RETENIR ABSOLUMENT","color":"green"},
  {"type":"box","content":"Gènes liés → crossing-over → 4 phénotypes (2P + 2R) → d = (R/Total)×100 → d < 50 %","color":"green"}
]}}]}</ui>

هاد 4 خطوات كافية باش تحل أي تمرين ديال gènes liés فـ BAC. واش واضحة ولا غادي نزيد نعطي مثال تطبيقي؟
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2024_rattrapage",
  "subject": "SVT",
  "year": 2024,
  "session": "Rattrapage",
  "exam_title": "SVT 2024 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 3,
  "question_content": "En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis montrer la relation entre le taux plasmatique de la progranuline et l'état de santé de la personne."
}
```

---

## 6. T6 — coaching : BUG — après tableau, ré-ouvrir un examen

**Message utilisateur :**
> Merci pour cette explication. Maintenant donne-moi un exercice BAC SVT sur ce même thème pour m'entraîner.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2024_rattrapage",
  "subject": "SVT",
  "year": 2024,
  "session": "Rattrapage",
  "exam_title": "SVT 2024 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 3,
  "question_content": "En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis montrer la relation entre le taux plasmatique de la progranuline et l'état de santé de la personne."
}
```

**Tag `<exam_exercise>` émis** : `gènes liés test-cross distance génétique brassage intrachromosomique BAC SVT`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés test-cross distance génétique brassage intrachromosomique BAC SVT'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (188 chars — extrait) :**
```
واخا! دابا غادي نفتح ليك تمرين BAC رسمي على gènes liés باش تطبق هاد la méthode.

<exam_exercise>gènes liés test-cross distance génétique brassage intrachromosomique BAC SVT</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

---

## 7. T7 — coaching : verrou matière (doit rester SVT)

**Message utilisateur :**
> Parfait. Ferme celui-ci et ouvre-moi un AUTRE exercice BAC — peu importe le thème — mais reste bien en SVT (surtout pas de Physique ni Chimie).

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2025_rattrapage",
  "subject": "SVT",
  "year": 2025,
  "session": "Rattrapage",
  "exam_title": "SVT 2025 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous aidant d'un échiquier de croisement."
}
```

**Tag `<exam_exercise>` émis** : `SVT BAC exercice domaine 1 2 3 4`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2022 Rattrapage** — _Exercice 3 | En vous basant sur les documents 2 et 3, comparez la concentration en métaux lourds dans les lixiviats dans les deux déc_ (matière : **SVT**)
- log backend :
  - `primary: tag='SVT BAC exercice domaine 1 2 3 4'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (161 chars — extrait) :**
```
D'accord, je ferme tout et je t'ouvre un autre exercice BAC SVT officiel sur un thème différent.

<exam_exercise>SVT BAC exercice domaine 1 2 3 4</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2022_rattrapage",
  "subject": "SVT",
  "year": 2022,
  "session": "Rattrapage",
  "exam_title": "SVT 2022 Rattrapage",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 2,
  "question_content": "En vous basant sur les documents 2 et 3, comparez la concentration en métaux lourds dans les lixiviats dans les deux décharges et expliquez la composition de lixiviat de la décharge de Marrakech. (1.5pt)"
}
```

---

**Score final : 7/7** — 🎉 TOUT VERT
