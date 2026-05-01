# Test MULTI-TOURS — BUG exam switch / genes liés / après tableau

_Généré le 2026-05-01 18:20:40_


Objectif : reproduire le scénario exact rapporté par l'utilisateur en jouant une conversation à 7 tours contre le vrai LLM DeepSeek et en simulant le backend (exam_bank + cascading retries) entre chaque tour.


## Score : **7/7** — 🎉 TOUT VERT


| # | Tour | Path | Action | Subject ouverte | Verdict |
|---|---|---|---|---|---|
| 1 | T1 — ouvrir un premier exercice BAC SVT (mitose) | `force_fallback_ok` | `open` | `SVT` | ✅ |
| 2 | T2 — un autre exercice BAC SVT (switch facile #1) | `primary_ok` | `open` | `SVT` | ✅ |
| 3 | T3 — encore un autre BAC SVT (switch facile #2) | `primary_ok` | `open` | `SVT` | ✅ |
| 4 | T4 — BUG RAPPORTÉ : génétique DEUX GÈNES LIÉS | `primary_ok` | `open` | `SVT` | ✅ |
| 5 | T5 — BUG RAPPORTÉ : retry → ouvre n'importe quoi | `primary_ok` | `open` | `SVT` | ✅ |
| 6 | T6 — demande tableau (whiteboard) | `no_action` | `stay` | `—` | ✅ |
| 7 | T7 — BUG RAPPORTÉ : après tableau, ré-ouvrir un examen | `primary_ok` | `open` | `SVT` | ✅ |

---

## 1. T1 — ouvrir un premier exercice BAC SVT (mitose)

**Message utilisateur :**
> Salut ! Je suis en 2BAC SVT BIOF. Peux-tu m'ouvrir un exercice BAC SVT sur la mitose ou la division cellulaire pour m'entraîner ?

**État AVANT ce tour :**
```json
null (aucun examen ouvert)
```

**Tag `<exam_exercise>` émis** : `(aucun)`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `force_fallback_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `AI emitted <ui> show_board (whiteboard)`
  - `force_fallback: query='Salut ! Je suis en 2BAC SVT BIOF. Peux-tu m'ouvrir un exerci' subject='SVT' subject_from_user=True`
  - `force_fallback_ok: SVT 2025 Rattrapage`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromo' ne contient aucun de ['mitose', 'cellulaire', 'cellule', 'chromosome'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (2702 chars — extrait) :**
```
Bonjour ! Ravie de t'aider à t'entraîner pour le BAC SVT.

Avant de te proposer un exercice, je dois te faire une petite précision importante concernant ton programme.

Le sujet de la **mitose** et de la **division cellulaire** fait-il partie de ton programme de **2BAC Sciences Physiques (PC) BIOF** ?

Dans le programme officiel du 2BAC PC, le domaine "Information génétique et lois statistiques de transmission" (25% de l'examen) inclut bien la **mitose**, la **méiose**, le **cycle cellulaire**, le **caryotype**, etc. Donc oui, c'est au programme pour toi !

Je vais donc te proposer un exercice type BAC sur la mitose. Prêt à commencer ?

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"🎯 Exercice BAC : La Mitose","lines":[
  {"type":"illustration","icon":"🧬","content":"Division cellulaire — la mitose"},
  {"type":"text","content":"Voici un extrait d'un sujet national. Lis attentivement et réponds aux questions."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📝 Document : Observation microscopique"},
  {"type":"text","content":"On observe au microscope des cellules d'une racine d'oignon en division. On distingue les phases suivantes :"},
  {"type":"text","content":"1. Phase A : Les chromosomes sont alignés au centre de la cellule."},
  {"type":"text","content":"2. Phase B : Les chromatides sœurs se séparent et migrent vers les pôles."},
  {"type":"text","content":"3. Phase C : Les chromosomes sont décondensés, la membrane nucléaire se reforme."},
  {"type":"text","content":"4. Phase D : Les chromosomes sont visibles, la membrane nucléaire disparaît."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"❓ Questions (type BAC)"},
  {"type":"step","label":"1","content":"Nomme chaque phase (A, B, C, D) de la mitose."},
  {"type":"step","label":"2","content":"Classe ces phases dans l'ordre chronologique de la mitose."},
  {"type":"step","label":"3","content":"Décris brièvement ce qui se passe pendant la phase B."},
  {"type":"step","label":"4","content":"Quel est le rôle principal de la mitose dans un organisme ?"},
  {"type":"separator","content":""},
  {"type":"box","content":"📝 À NOTER : La mitose permet la croissance et le renouvellement cellulaire. Elle produit 2 cellules filles identiques à la cellule mère (même nombre de chromosomes).","color":"orange"}
]}}]}</ui>

<suggestions>[
  {"label":"Je réponds aux questions","prompt":"Je vais essayer de répondre aux questions sur la mitose."},
…[tronqué]
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

## 2. T2 — un autre exercice BAC SVT (switch facile #1)

**Message utilisateur :**
> Super ! Maintenant ferme celui-ci et donne-moi un AUTRE exercice BAC SVT sur la génétique mendélienne (monohybridisme ou dihybridisme).

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

**Tag `<exam_exercise>` émis** : `génétique mendélienne monohybridisme dihybridisme croisement drosophile`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2019 Rattrapage** — _Exercice 2 | A partir des résultats du croisement 1 et 2, donnez les génotypes probables des chiens normaux et des chiens hairless, j_ (matière : **SVT**)
- log backend :
  - `primary: tag='génétique mendélienne monohybridisme dihybridisme croisement drosophile'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (218 chars — extrait) :**
```
D'accord, je ferme l'exercice sur la mitose et je t'ouvre un nouvel exercice BAC SVT sur la génétique mendélienne.

<exam_exercise>génétique mendélienne monohybridisme dihybridisme croisement drosophile</exam_exercise>
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

## 3. T3 — encore un autre BAC SVT (switch facile #2)

**Message utilisateur :**
> Merci. Ferme et ouvre-moi un AUTRE exercice BAC SVT, par exemple sur les chaînes de transmission génétique ou l'ADN.

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

**Tag `<exam_exercise>` émis** : `ADN réplication transcription traduction synthèse protéines`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2017 Rattrapage** — _Exercice 2 | Expliquez les résultats de l'expérience du document 1, en justifiant votre réponse à l'aide d'un schéma adéquat du phéno_ (matière : **SVT**)
- log backend :
  - `primary: tag='ADN réplication transcription traduction synthèse protéines'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 2 | Expliquez les résultats de l'expérience du document 1, en justifian' ne contient aucun de ['gen', 'adn', 'allele', 'chromosome', 'proteine'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (212 chars — extrait) :**
```
D'accord, je ferme l'exercice précédent et je t'ouvre un nouvel exercice BAC SVT sur l'ADN et la transmission génétique.

<exam_exercise>ADN réplication transcription traduction synthèse protéines</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2017_rattrapage",
  "subject": "SVT",
  "year": 2017,
  "session": "Rattrapage",
  "exam_title": "SVT 2017 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 2,
  "question_content": "Expliquez les résultats de l'expérience du document 1, en justifiant votre réponse à l'aide d'un schéma adéquat du phénomène biologique mis en évidence."
}
```

---

## 4. T4 — BUG RAPPORTÉ : génétique DEUX GÈNES LIÉS

**Message utilisateur :**
> Parfait. Maintenant je veux un autre exercice BAC SVT sur la génétique avec DEUX GÈNES LIÉS (linkage / gènes liés sur le même chromosome, brassage intrachromosomique). Ferme celui-ci et ouvre le nouveau.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2017_rattrapage",
  "subject": "SVT",
  "year": 2017,
  "session": "Rattrapage",
  "exam_title": "SVT 2017 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 2,
  "question_content": "Expliquez les résultats de l'expérience du document 1, en justifiant votre réponse à l'aide d'un schéma adéquat du phénomène biologique mis en évidence."
}
```

**Tag `<exam_exercise>` émis** : `gènes liés linkage brassage intrachromosomique recombinaison carte factorielle drosophile`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2020 Normale** — _Exercice 3 | 1. En exploitant les résultats du premier et du deuxième croisement, déterminez le mode de transmission des deux caractè_ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés linkage brassage intrachromosomique recombinaison carte factorielle d'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 3 | 1. En exploitant les résultats du premier et du deuxième croisement' ne contient aucun de ['lie', 'linkage', 'intrachromos', 'brassage', 'hybrid'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (249 chars — extrait) :**
```
D'accord, je ferme l'exercice précédent et je t'ouvre un exercice BAC SVT sur les gènes liés et le brassage intrachromosomique.

<exam_exercise>gènes liés linkage brassage intrachromosomique recombinaison carte factorielle drosophile</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2020_normale",
  "subject": "SVT",
  "year": 2020,
  "session": "Normale",
  "exam_title": "SVT 2020 Normale",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 6,
  "question_content": "1. En exploitant les résultats du premier et du deuxième croisement, déterminez le mode de transmission des deux caractères étudiés."
}
```

---

## 5. T5 — BUG RAPPORTÉ : retry → ouvre n'importe quoi

**Message utilisateur :**
> Ça n'a pas marché. Donne-moi alors un autre exercice BAC SVT, peu importe le thème tant que c'est SVT.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2020_normale",
  "subject": "SVT",
  "year": 2020,
  "session": "Normale",
  "exam_title": "SVT 2020 Normale",
  "exercise_name": "Exercice 3",
  "question_number": 1,
  "question_total": 6,
  "question_content": "1. En exploitant les résultats du premier et du deuxième croisement, déterminez le mode de transmission des deux caractères étudiés."
}
```

**Tag `<exam_exercise>` émis** : `consommation matière organique flux énergie respiration cellulaire`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2020 Rattrapage** — _Exercice 1 | En exploitant le document 1, déduisez les conditions de synthèse d'ATP au niveau des mitochondries (1.25 pts)_ (matière : **SVT**)
- log backend :
  - `primary: tag='consommation matière organique flux énergie respiration cellulaire'`
  - `subject from pre_text -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (145 chars — extrait) :**
```
D'accord, je réessaie avec un autre thème SVT.

<exam_exercise>consommation matière organique flux énergie respiration cellulaire</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2020_rattrapage",
  "subject": "SVT",
  "year": 2020,
  "session": "Rattrapage",
  "exam_title": "SVT 2020 Rattrapage",
  "exercise_name": "Exercice 1",
  "question_number": 1,
  "question_total": 1,
  "question_content": "En exploitant le document 1, déduisez les conditions de synthèse d'ATP au niveau des mitochondries (1.25 pts)"
}
```

---

## 6. T6 — demande tableau (whiteboard)

**Message utilisateur :**
> OK. Explique-moi plutôt au TABLEAU la méthode pour résoudre un croisement avec deux gènes LIÉS : test-cross, recombinants, parentaux, carte génétique.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2020_rattrapage",
  "subject": "SVT",
  "year": 2020,
  "session": "Rattrapage",
  "exam_title": "SVT 2020 Rattrapage",
  "exercise_name": "Exercice 1",
  "question_number": 1,
  "question_total": 1,
  "question_content": "En exploitant le document 1, déduisez les conditions de synthèse d'ATP au niveau des mitochondries (1.25 pts)"
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

**Réponse LLM (2862 chars — extrait) :**
```
Parfait ! Je vais t'expliquer la méthode complète pour résoudre un croisement avec deux gènes liés, étape par étape, comme au BAC.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"🧬 Méthode BAC : Deux gènes liés (Linkage)","lines":[
  {"type":"illustration","icon":"🧬","content":"Brassage intrachromosomique — gènes liés"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📌 Étape 1 : Identifier les parentaux et les recombinés"},
  {"type":"text","content":"Dans un test-cross (F1 × double récessif), les phénotypes les PLUS FRÉQUENTS sont les PARENTAUX. Les MOINS FRÉQUENTS sont les RECOMBINÉS."},
  {"type":"box","content":"🔑 Parentaux = combinaisons des allèles des parents P1 et P2\nRecombinés = nouvelles combinaisons issues du crossing-over","color":"green"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📌 Étape 2 : Calculer la distance génétique"},
  {"type":"text","content":"Distance (en cM) = (Nombre de recombinés / Total des individus) × 100"},
  {"type":"box","content":"d = (R / T) × 100   (1 cM = 1% de recombinaison)","color":"green"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📌 Étape 3 : Déterminer les gamètes de F1"},
  {"type":"text","content":"Si distance = d cM, alors :"},
  {"type":"text","content":"• Gamètes parentaux : chacun (100 - d)/2 %"},
  {"type":"text","content":"• Gamètes recombinés : chacun d/2 %"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📌 Étape 4 : Construire la carte factorielle"},
  {"type":"text","content":"Placer les gènes sur un axe avec la distance calculée entre eux."},
  {"type":"box","content":"Exemple : Gène A ——— 12 cM ——— Gène B","color":"orange"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"⚠️ Piège BAC"},
  {"type":"warning","content":"Ne JAMAIS confondre gènes liés et indépendants !\n• Liés : 4 phénotypes avec 2 fréquences différentes (parentaux > recombinés)\n• Indépendants : 4 phénotypes équiprobables (25% chacun)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"💡 Astuce mémoire"},
  {"type":"tip","content":"P = Parentaux = Plus fréquents\nR = Recombinés = Rares\nDistance = (R/T)×100 → plus R est grand, plus les gènes sont éloignés."},
  {"type":"separator","content":""},
  {"type":"box","content":"📝 À RETENIR : Test-cross → parentaux > recombinés → distance = % de recombinaison → carte génétique","color":"orange"}
]}}]}</ui>

**Résumé oral :*
…[tronqué]
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2020_rattrapage",
  "subject": "SVT",
  "year": 2020,
  "session": "Rattrapage",
  "exam_title": "SVT 2020 Rattrapage",
  "exercise_name": "Exercice 1",
  "question_number": 1,
  "question_total": 1,
  "question_content": "En exploitant le document 1, déduisez les conditions de synthèse d'ATP au niveau des mitochondries (1.25 pts)"
}
```

---

## 7. T7 — BUG RAPPORTÉ : après tableau, ré-ouvrir un examen

**Message utilisateur :**
> Merci pour l'explication. Maintenant donne-moi un exercice BAC SVT sur ce même thème (génétique, gènes liés ou brassage) pour que je m'entraîne.

**État AVANT ce tour :**
```json
{
  "exam_id": "svt_2020_rattrapage",
  "subject": "SVT",
  "year": 2020,
  "session": "Rattrapage",
  "exam_title": "SVT 2020 Rattrapage",
  "exercise_name": "Exercice 1",
  "question_number": 1,
  "question_total": 1,
  "question_content": "En exploitant le document 1, déduisez les conditions de synthèse d'ATP au niveau des mitochondries (1.25 pts)"
}
```

**Tag `<exam_exercise>` émis** : `gènes liés brassage intrachromosomique test-cross distance génétique carte factorielle`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés brassage intrachromosomique test-cross distance génétique carte facto'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (213 chars — extrait) :**
```
D'accord, je t'ouvre un exercice BAC SVT sur les gènes liés et le brassage intrachromosomique.

<exam_exercise>gènes liés brassage intrachromosomique test-cross distance génétique carte factorielle</exam_exercise>
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

**Score final : 7/7** — 🎉 TOUT VERT
