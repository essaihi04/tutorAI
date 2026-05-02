# Test MULTI-TOURS — BUG exam switch / genes liés / après tableau

_Généré le 2026-05-01 18:58:47_


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

**Réponse LLM (4342 chars — extrait) :**
```
Bonjour ! Ravie de t'aider à t'entraîner pour le BAC ! 😊

Avant de te proposer un exercice, je dois faire une petite vérification importante concernant le programme.

Le sujet que tu demandes — **la mitose / la division cellulaire** — fait partie du programme du **2BAC Sciences de la Vie et de la Terre (SVT track)**. Cependant, toi tu es en **2BAC Sciences Physiques (PC) BIOF**, et le programme de SVT en PC est **différent** et **plus réduit**.

En SVT PC, le **cycle cellulaire** et la **mitose** sont effectivement abordés, mais uniquement dans le cadre du **Domaine 2 — Information génétique et lois statistiques de transmission** (25% de l'examen). Ils servent de base pour comprendre la réplication de l'ADN, la méiose et la transmission des caractères héréditaires.

Je vais donc te proposer un **exercice BAC adapté au programme PC** qui porte sur la **mitose** en lien avec la **réplication de l'ADN** et le **maintien de l'information génétique**.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"🎯 Exercice BAC — Mitose & Information génétique","lines":[
  {"type":"illustration","icon":"🧬","content":"Division cellulaire et maintien du caryotype"},
  {"type":"separator","content":""},
  {"type":"title","icon":"📝","content":"Sujet BAC — La mitose et la stabilité génétique"},
  {"type":"text","content":"Le document ci-dessous représente les différentes phases de la mitose d'une cellule diploïde à 2n = 4 chromosomes."},
  {"type":"separator","content":""},
  {"type":"subtitle","icon":"🔬","content":"Document : Schéma des phases de la mitose"},
  {"type":"text","content":"Phase 1 : Les chromosomes sont visibles, chacun formé de deux chromatides sœurs reliées par un centromère. La membrane nucléaire disparaît."},
  {"type":"text","content":"Phase 2 : Les chromosomes se placent sur le plan équatorial de la cellule."},
  {"type":"text","content":"Phase 3 : Les chromatides sœurs se séparent et migrent vers les pôles opposés."},
  {"type":"text","content":"Phase 4 : La membrane nucléaire se reforme autour de chaque lot de chromosomes. La cellule se divise."},
  {"type":"separator","content":""},
  {"type":"subtitle","icon":"❓","content":"Questions"},
  {"type":"step","label":"1","content":"Nomme les quatre phases de la mitose dans l'ordre chronologique."},
  {"type":"step","label":"2","content":"Explique comment la mitose assure la stabilité du caryotype (même nombre de chromosomes et même information génétique) entre la cellule mère et l
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

**Réponse LLM (211 chars — extrait) :**
```
D'accord, je ferme l'exercice précédent et je t'ouvre un nouvel exercice BAC sur la génétique mendélienne !

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

**Tag `<exam_exercise>` émis** : `ADN réplication transcription traduction information génétique`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2025 Rattrapage** — _Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromosomique des résultats des croisements 1 et 2 en vous _ (matière : **SVT**)
- log backend :
  - `primary: tag='ADN réplication transcription traduction information génétique'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 3 | En se basant sur les données 1 et 2, donner l'interprétation chromo' ne contient aucun de ['gen', 'adn', 'allele', 'chromosome', 'proteine'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (215 chars — extrait) :**
```
D'accord, je ferme l'exercice précédent et je t'ouvre un nouvel exercice BAC SVT sur l'ADN et la transmission génétique.

<exam_exercise>ADN réplication transcription traduction information génétique</exam_exercise>
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

## 4. T4 — BUG RAPPORTÉ : génétique DEUX GÈNES LIÉS

**Message utilisateur :**
> Parfait. Maintenant je veux un autre exercice BAC SVT sur la génétique avec DEUX GÈNES LIÉS (linkage / gènes liés sur le même chromosome, brassage intrachromosomique). Ferme celui-ci et ouvre le nouveau.

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

**Tag `<exam_exercise>` émis** : `gènes liés linkage brassage intrachromosomique crossing-over carte factorielle distance recombinaison`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2024 Rattrapage** — _Exercice 2 | En se basant sur les données du document 1, décrire le mode d'action de la progranuline sur les cellules nerveuses puis _ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés linkage brassage intrachromosomique crossing-over carte factorielle d'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 2 | En se basant sur les données du document 1, décrire le mode d'actio' ne contient aucun de ['lie', 'linkage', 'intrachromos', 'brassage', 'hybrid'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (271 chars — extrait) :**
```
D'accord, je ferme l'exercice précédent et je t'ouvre un exercice BAC SVT sur les gènes liés (linkage) et le brassage intrachromosomique.

<exam_exercise>gènes liés linkage brassage intrachromosomique crossing-over carte factorielle distance recombinaison</exam_exercise>
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

## 5. T5 — BUG RAPPORTÉ : retry → ouvre n'importe quoi

**Message utilisateur :**
> Ça n'a pas marché. Donne-moi alors un autre exercice BAC SVT, peu importe le thème tant que c'est SVT.

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

**Tag `<exam_exercise>` émis** : `SVT géodynamique interne chaîne de montagnes subduction`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2020 Rattrapage** — _Exercice 5 | A partir du document 1, dégagez quatre indices indiquant que les Andes est une chaîne de subduction. (1 pt)_ (matière : **SVT**)
- log backend :
  - `primary: tag='SVT géodynamique interne chaîne de montagnes subduction'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS

**Réponse LLM (143 chars — extrait) :**
```
Pas de problème, je t'ouvre un autre exercice BAC SVT !

<exam_exercise>SVT géodynamique interne chaîne de montagnes subduction</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2020_rattrapage",
  "subject": "SVT",
  "year": 2020,
  "session": "Rattrapage",
  "exam_title": "SVT 2020 Rattrapage",
  "exercise_name": "Exercice 5",
  "question_number": 1,
  "question_total": 3,
  "question_content": "A partir du document 1, dégagez quatre indices indiquant que les Andes est une chaîne de subduction. (1 pt)"
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
  "exercise_name": "Exercice 5",
  "question_number": 1,
  "question_total": 3,
  "question_content": "A partir du document 1, dégagez quatre indices indiquant que les Andes est une chaîne de subduction. (1 pt)"
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

**Réponse LLM (3587 chars — extrait) :**
```
Bien sûr ! Je vais t'expliquer la méthode complète pour résoudre un croisement avec deux gènes liés, étape par étape, comme au BAC.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"🧬 Méthode BAC — Gènes liés (Linkage)","lines":[
  {"type":"illustration","icon":"🧬","content":"Deux gènes sur le même chromosome — Brassage intrachromosomique"},
  {"type":"separator","content":""},
  {"type":"title","icon":"🎯","content":"1. Reconnaître un cas de gènes liés"},
  {"type":"text","content":"L'énoncé mentionne : « gènes situés sur le même chromosome », « linkage », « distance en cM », « crossing-over », ou les résultats du test-cross ne suivent PAS les proportions 25%-25%-25%-25% du dihybridisme indépendant."},
  {"type":"separator","content":""},
  {"type":"title","icon":"🔑","content":"2. Les 4 types de gamètes du dihybride F1"},
  {"type":"text","content":"Un individu double hétérozygote (ex: AaBb) produit 4 types de gamètes, MAIS avec des proportions INÉGALES :"},
  {"type":"box","content":"🔸 2 gamètes PARENTAUX (les plus fréquents) : chacun (100 - d)/2 %\n🔸 2 gamètes RECOMBINÉS (les moins fréquents) : chacun d/2 %\n👉 d = distance en cM entre les deux gènes","color":"green"},
  {"type":"separator","content":""},
  {"type":"title","icon":"📊","content":"3. Identifier parentaux vs recombinés dans le test-cross"},
  {"type":"step","label":"1","content":"Croise le F1 double hétérozygote avec un homozygote récessif (test-cross)."},
  {"type":"step","label":"2","content":"Observe les 4 phénotypes de la descendance et leurs effectifs."},
  {"type":"step","label":"3","content":"Les 2 phénotypes les PLUS nombreux = parentaux (issus des gamètes parentaux)."},
  {"type":"step","label":"4","content":"Les 2 phénotypes les MOINS nombreux = recombinés (issus des gamètes recombinés)."},
  {"type":"separator","content":""},
  {"type":"title","icon":"📐","content":"4. Calcul de la distance génétique (carte factorielle)"},
  {"type":"math","content":"d = \\frac{\\text{Nombre de recombinés}}{\\text{Effectif total}} \\times 100 \\quad (\\text{en cM})"},
  {"type":"box","content":"Exemple : 180 parentaux + 20 recombinés sur 200 individus → d = 20/200 × 100 = 10 cM","color":"orange"},
  {"type":"separator","content":""},
  {"type":"title","icon":"⚠️","content":"5. Piège BAC — Ne pas confondre"},
  {"type":"warning","content":"⚠️ Gènes indépendants → 4 gamètes équiprobables (25% chacun) → test-cross donne 25%-25%-25%-25%\n⚠️ Gènes liés → 2 gamètes parentaux 
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
  "exercise_name": "Exercice 5",
  "question_number": 1,
  "question_total": 3,
  "question_content": "A partir du document 1, dégagez quatre indices indiquant que les Andes est une chaîne de subduction. (1 pt)"
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
  "exercise_name": "Exercice 5",
  "question_number": 1,
  "question_total": 3,
  "question_content": "A partir du document 1, dégagez quatre indices indiquant que les Andes est une chaîne de subduction. (1 pt)"
}
```

**Tag `<exam_exercise>` émis** : `gènes liés brassage intrachromosomique crossing-over test-cross carte factorielle drosophile`

**Simulation backend :**
- subject_hint = `SVT` (subject_from_user=True)
- path_taken = `primary_ok`
- panel_action = `open`
- examen ouvert = **SVT 2022 Rattrapage** — _Exercice 2 | En exploitant les données du document 1, montrez la relation : caractère « couleur des cheveux » - protéine. (1 pt)_ (matière : **SVT**)
- log backend :
  - `primary: tag='gènes liés brassage intrachromosomique crossing-over test-cross carte factoriell'`
  - `subject from tag -> SVT`
  - `primary_ok: 1 ex found`

**Checks :**
- ✅ PASS (mais 1 warning(s))
- ⚠️ topic opened='Exercice 2 | En exploitant les données du document 1, montrez la relation : cara' ne contient aucun de ['gen', 'hybrid', 'croisement', 'brassage'] (⚠️ couverture du corpus / scoring de search_full_exercises)

**Réponse LLM (224 chars — extrait) :**
```
Avec plaisir ! Je t'ouvre un exercice BAC SVT sur les gènes liés et le brassage intrachromosomique.

<exam_exercise>gènes liés brassage intrachromosomique crossing-over test-cross carte factorielle drosophile</exam_exercise>
```

**État APRÈS ce tour :**
```json
{
  "exam_id": "svt_2022_rattrapage",
  "subject": "SVT",
  "year": 2022,
  "session": "Rattrapage",
  "exam_title": "SVT 2022 Rattrapage",
  "exercise_name": "Exercice 2",
  "question_number": 1,
  "question_total": 5,
  "question_content": "En exploitant les données du document 1, montrez la relation : caractère « couleur des cheveux » - protéine. (1 pt)"
}
```

---

**Score final : 7/7** — 🎉 TOUT VERT
