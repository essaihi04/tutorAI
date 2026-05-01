# Test — balise `<exam_exercise>` mal formée (bug transcript pollution)

_Généré le 2026-05-01 18:57:47_


**Contexte :** transcript utilisateur où l'IA annonce un exercice BAC SVT sur la **pollution** mais le panneau ne s'ouvre jamais, obligeant l'utilisateur à répéter 3 fois, puis à demander une explication au tableau d'une « question 2 » que l'IA ne peut pas identifier (le panneau n'a jamais contenu d'exercice).


## Score : **4/4** — 🎉 TOUT VERT


| Variante | Tag extrait | Path | Action | Examen ouvert |
|---|---|---|---|---|
| V1 — aucune balise (msg 1 du transcript) | `(rien)` | `force_fallback_ok` | `open` | SVT 2025 Normale |
| V2 — balise fermee mais CONTENU VIDE | `(rien)` | `force_fallback_ok` | `open` | SVT 2025 Normale |
| V3 — balise OUVERTE, NON FERMEE (msg 3 du transcript) | `(rien)` | `force_fallback_ok` | `open` | SVT 2025 Normale |
| V4 — balise ouverte + contenu valide mais NON FERMEE | `pollution environnement ecosysteme matie` | `primary_ok` | `open` | SVT 2019 Normale |

---

## V1 — aucune balise (msg 1 du transcript)

**Réponse LLM simulée :**
```
D'accord Ferdaous ! Je t'ouvre un exercice du BAC marocain sur la **pollution** (SVT - Domaine 3 : Utilisation des matières organiques et inorganiques) pour t'entraîner. Vas-y, essaye de répondre avant de regarder la correction ! 💪
```

**Tag extrait par le regex du fix :** `(aucun)`

**Simulation backend :**
- panel_action = `open`
- path = `force_fallback_ok`
- examen ouvert = **SVT 2025 Normale** — __ (matière : **SVT**)
- log :
  - `tag_extracted=None`
  - `force_fallback_ok: SVT 2025 Normale — `

**Verdict :** ✅ PASS

---

## V2 — balise fermee mais CONTENU VIDE

**Réponse LLM simulée :**
```
D'accord ! Je t'ouvre un exercice BAC SVT sur la pollution.
<exam_exercise></exam_exercise>
Prends ton temps pour répondre.
```

**Tag extrait par le regex du fix :** `(aucun)`

**Simulation backend :**
- panel_action = `open`
- path = `force_fallback_ok`
- examen ouvert = **SVT 2025 Normale** — __ (matière : **SVT**)
- log :
  - `tag_extracted=None`
  - `force_fallback_ok: SVT 2025 Normale — `

**Verdict :** ✅ PASS

---

## V3 — balise OUVERTE, NON FERMEE (msg 3 du transcript)

**Réponse LLM simulée :**
```
Très bien Ferdaous ! Puisque tu travailles actuellement sur la **pollution** (SVT - Domaine 3), je vais te proposer un exercice de type BAC marocain sur ce thème, comme tu l'as demandé. Prends le temps de réfléchir et de répondre, puis je te donnerai la **correction détaillée** étape par étape avec un tableau récapitulatif. 💪

<exam_exercise>
```

**Tag extrait par le regex du fix :** `(aucun)`

**Simulation backend :**
- panel_action = `open`
- path = `force_fallback_ok`
- examen ouvert = **SVT 2025 Normale** — __ (matière : **SVT**)
- log :
  - `tag_extracted=None`
  - `force_fallback_ok: SVT 2025 Normale — `

**Verdict :** ✅ PASS

---

## V4 — balise ouverte + contenu valide mais NON FERMEE

**Réponse LLM simulée :**
```
D'accord ! Je t'ouvre un exercice BAC SVT sur la pollution.
<exam_exercise>pollution environnement ecosysteme matiere organique degradation</exam_exercise
```

**Tag extrait par le regex du fix :** `pollution environnement ecosysteme matiere organique degradation`

**Simulation backend :**
- panel_action = `open`
- path = `primary_ok`
- examen ouvert = **SVT 2019 Normale** — __ (matière : **SVT**)
- log :
  - `tag_extracted='pollution environnement ecosysteme matiere organique degradation'`
  - `primary_ok: SVT 2019 Normale — `

**Verdict :** ✅ PASS

---

**Score final : 4/4** — 🎉 TOUT VERT
