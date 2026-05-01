# Test — ROUTAGE DE MATIÈRE pour les demandes d'exercice BAC

_Généré le 2026-05-01 16:29:48_


Objectif : confirmer que quand l'utilisateur demande un exercice BAC dans une matière précise (SVT, Math, Physique…), l'AI ouvre bien un exercice de cette matière, et pas une autre.


## Score global : **28/28** — 🎉 TOUT VERT


| # | Scénario | Mode | Demandé | Résolu | Match | Verdict |
|---|---|---|---|---|---|---|
| 1 | A1 • LIBRE — exercice BAC en SVT (mitose) | `libre` | SVT | SVT | SVT ✅ | 4/4 ✅ |
| 2 | A2 • LIBRE — exercice BAC SVT (génétique mendelienne) | `libre` | SVT | SVT | SVT ✅ | 4/4 ✅ |
| 3 | A3 • LIBRE — exercice BAC SVT (géologie / tectonique) | `libre` | SVT | SVT | SVT ✅ | 4/4 ✅ |
| 4 | A4 • LIBRE — exercice BAC SVT (consommation matière organique) | `libre` | SVT | SVT | SVT ✅ | 4/4 ✅ |
| 5 | B1 • COACHING SVT — exercice BAC sur génétique | `coaching` | SVT | SVT | SVT ✅ | 4/4 ✅ |
| 6 | C1 • LIBRE — exercice BAC Maths (complexes) [contrôle] | `libre` | Mathematiques | Mathématiques | Mathematiques ✅ | 4/4 ✅ |
| 7 | C2 • LIBRE — exercice BAC Physique (RLC) [contrôle] | `libre` | Physique | Physique | Physique-Chimie ✅ | 4/4 ✅ |

---

## 1. A1 • LIBRE — exercice BAC en SVT (mitose)

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **SVT**
- **Temps LLM** : 10.8s  •  **Réponse** : 2334 chars

**Message envoyé :** > Donne-moi un exercice BAC en SVT sur la mitose. Je veux pouvoir m'entraîner sur la division cellulaire.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `(vide)`

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='') = None
- step3: _detect_subject_from_text(pre_text len=0) = None
- step4: _infer_subject_from_context() = SVT
- final: subject_hint=SVT (from_user=False)
- **➡ Matière finale : 'SVT'**

### Exercice retourné par exam_bank
- **subject** : `SVT`
- **exam_label** : SVT 2025 Rattrapage
- **exercise_name** : Exercice 3
- **topic** : Génétique des populations
- **# questions** : 2

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | (aucun tag — la prod tombera sur force_exam_panel) |
| 2 | Matière résolue == SVT (accent-insensitive) | ✅ PASS | résolu : 'SVT' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en SVT (bug original : SVT → PC) | ✅ PASS | subject='SVT', exam='SVT 2025 Rattrapage', topic='Génétique des populations' |

### Réponse LLM (2334 chars — extrait)
```
Bien sûr ! Je te propose un exercice type BAC sur la mitose. Prends une feuille, note tes réponses, et on corrigera ensemble après.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Exercice BAC — Mitose (Division cellulaire)","lines":[
  {"type":"title","content":"🧬 Exercice : La mitose et ses étapes"},
  {"type":"separator","content":""},
  {"type":"text","content":"**Document 1** : On observe au microscope des cellules d'une racine d'oignon en division. On distingue les phases suivantes : A, B, C, D, E."},
  {"type":"text","content":"**Document 2** : La quantité d'ADN par cellule (en unités arbitraires) au cours du temps est donnée ci-dessous."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📝 Questions (10 points)"},
  {"type":"step","label":"1","content":"Nomme les phases A, B, C, D, E de la mitose dans l'ordre chronologique. (2 pts)"},
  {"type":"step","label":"2","content":"Décris brièvement ce qui se passe dans chaque phase. (3 pts)"},
  {"type":"step","label":"3","content":"Sur le graphique de la quantité d'ADN, repère par des lettres les moments correspondant à : la phase G1, la phase S, la phase G2, la mitose. (2 pts)"},
  {"type":"step","label":"4","content":"Explique pourquoi la quantité d'ADN double avant la mitose puis chute brutalement. (2 pts)"},
  {"type":"step","label":"5","content":"Quel est le rôle biologique de la mitose ? Donne un exemple. (1 pt)"},
  {"type":"separator","content":""},
  {"type":"box","content":"💡 **Conseil** : Dessine d'abord les phases sur un brouillon, puis réponds aux questions une par une.","color":"orange"}
]}}]}</ui>

Maintenant, prends ton temps pour répondre. Dis-moi quand tu es prêt(e) à corriger, ou si tu veux que je t'aide sur une question en particulier.

<suggestions>[
  {"label":"Je suis prêt(e) à corriger","prompt":"Je suis prêt(e) à corriger l'exercice sur la mitose","icon":"✅"},
  {"label":"Aide-moi sur la question 1","prompt":"Aide-moi à répondre à la question 1 sur les phases de la mitose","icon":"🔬"},
  {"label":"Explique le graphique ADN","prompt":"Explique-moi le graphique de la quantité d'ADN pendant le cycle cellulaire","icon":"📊"},
  {"label":"Je ne sais pas par où commencer","prompt":"Je ne sais pas par où commencer pour cet exercice sur la mitose","icon":"🤔"}
]</suggestions>
```

---

## 2. A2 • LIBRE — exercice BAC SVT (génétique mendelienne)

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **SVT**
- **Temps LLM** : 9.9s  •  **Réponse** : 1987 chars

**Message envoyé :** > Je voudrais un exercice du BAC SVT sur la génétique mendélienne, croisement dihybride, échiquier.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `génétique dihybridisme croisement échiquier F2`
- **Texte avant le tag (400 derniers chars)** :
  > idisme)

Excellent choix ! Le **dihybridisme** représente **~15% du domaine 2** (25% de l'examen SVT), soit environ **3-4 points sur 20**. C'est un incontournable du BAC.

Je te propose un exercice typique extrait du BAC national. Lance-le et essaie de le résoudre avant de regarder la correction :

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='génétique dihybridisme croisement échiquier F2') = SVT
- final: subject_hint=SVT (from_user=True)
- **➡ Matière finale : 'SVT'**

### Exercice retourné par exam_bank
- **subject** : `SVT`
- **exam_label** : SVT 2025 Rattrapage
- **exercise_name** : Exercice 3
- **topic** : Génétique des populations
- **# questions** : 2

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | contenu : 'génétique dihybridisme croisement échiquier F2' |
| 2 | Matière résolue == SVT (accent-insensitive) | ✅ PASS | résolu : 'SVT' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en SVT (bug original : SVT → PC) | ✅ PASS | subject='SVT', exam='SVT 2025 Rattrapage', topic='Génétique des populations' |

### Réponse LLM (1987 chars — extrait)
```
# Exercice BAC SVT — Génétique mendélienne (dihybridisme)

Excellent choix ! Le **dihybridisme** représente **~15% du domaine 2** (25% de l'examen SVT), soit environ **3-4 points sur 20**. C'est un incontournable du BAC.

Je te propose un exercice typique extrait du BAC national. Lance-le et essaie de le résoudre avant de regarder la correction :

<exam_exercise>génétique dihybridisme croisement échiquier F2</exam_exercise>

---

## 🧭 Avant de commencer, voici la méthode BAC à suivre :

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Méthode BAC — Dihybridisme","lines":[
  {"type":"title","content":"🎯 Résoudre un croisement dihybride en 5 étapes"},
  {"type":"step","label":"1","content":"Identifier les caractères et leurs allèles (dominant/récessif) d'après la F1"},
  {"type":"step","label":"2","content":"Écrire les génotypes des parents P1 et P2 (homozygotes)"},
  {"type":"step","label":"3","content":"Déterminer les gamètes de chaque parent (1 type si homozygote, 4 types si hétérozygote)"},
  {"type":"step","label":"4","content":"Construire l'échiquier de croisement F1×F1 (16 cases)"},
  {"type":"step","label":"5","content":"Compter les proportions phénotypiques F2 : 9/16, 3/16, 3/16, 1/16"},
  {"type":"separator","content":""},
  {"type":"box","content":"📝 À RETENIR : Si F1 100% [dominant,dominant] → parents homozygotes. F2 9:3:3:1 → gènes indépendants.","color":"orange"},
  {"type":"separator","content":""},
  {"type":"warning","content":"⚠️ PIÈGE BAC : Ne pas oublier que chaque gamète porte UN allèle de CHAQUE gène. Un dihybride produit 4 types de gamètes équiprobables (25% chacun)."},
  {"type":"tip","content":"💡 ASTUCE : Pour l'échiquier 16 cases, écris d'abord les 4 gamètes ♂ en haut et les 4 gamètes ♀ à gauche, puis remplis case par case."}
]}}]}</ui>

---

**Consigne :** Ouvre l'exercice ci-dessus, lis l'énoncé, et essaie de construire l'échiquier toi-même. Dis-moi quand tu as fini ou si tu bloques sur une étape !
```

---

## 3. A3 • LIBRE — exercice BAC SVT (géologie / tectonique)

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **SVT**
- **Temps LLM** : 19.4s  •  **Réponse** : 4146 chars

**Message envoyé :** > Donne-moi un sujet d'examen BAC SVT sur la tectonique des plaques, subduction, dorsale. Je révise la géologie.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `(vide)`

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='') = None
- step3: _detect_subject_from_text(pre_text len=0) = None
- step4: _infer_subject_from_context() = SVT
- final: subject_hint=SVT (from_user=False)
- **➡ Matière finale : 'SVT'**

### Exercice retourné par exam_bank
- **subject** : `SVT`
- **exam_label** : SVT 2020 Rattrapage
- **exercise_name** : Exercice 5
- **topic** : Géologie et tectonique des plaques
- **# questions** : 3

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | (aucun tag — la prod tombera sur force_exam_panel) |
| 2 | Matière résolue == SVT (accent-insensitive) | ✅ PASS | résolu : 'SVT' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en SVT (bug original : SVT → PC) | ✅ PASS | subject='SVT', exam='SVT 2020 Rattrapage', topic='Géologie et tectonique des plaques' |

### Réponse LLM (4146 chars — extrait)
```
# 🌍 Sujet BAC SVT — Géodynamique interne

Excellent choix ! La géodynamique interne représente **25% de l'épreuve SVT** (coefficient 5). C'est un domaine qui tombe **très régulièrement** au BAC national marocain.

Je vais te proposer un sujet complet, comme le jour J. Prends une feuille et un stylo, tu as **3h** pour le traiter.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Sujet BAC SVT — Géodynamique interne","lines":[
  {"type":"title","content":"📋 SUJET BAC — GÉODYNAMIQUE INTERNE (25% de l'épreuve)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"PARTIE 1 : Restitution des connaissances (5 points)"},
  {"type":"text","content":"1. Définis les termes suivants : lithosphère, asthénosphère, dorsale océanique, subduction."},
  {"type":"text","content":"2. Cite les trois types de mouvements des plaques lithosphériques et donne un exemple pour chacun."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"PARTIE 2 : Raisonnement scientifique (10 points)"},
  {"type":"text","content":"Document 1 : Carte des séismes et volcans actifs dans la région andine (Pérou-Chili)."},
  {"type":"text","content":"Document 2 : Coupe géologique de la fosse océanique du Pérou-Chili montrant la distribution des séismes (plan de Wadati-Benioff)."},
  {"type":"text","content":"Document 3 : Graphique de variation du flux thermique en fonction de la distance à la dorsale atlantique."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Questions (10 points) :"},
  {"type":"step","label":"1","content":"Analyse le document 1 : décris la répartition des séismes et volcans. (2 pts)"},
  {"type":"step","label":"2","content":"Exploite le document 2 : que montre le plan de Wadati-Benioff ? Quel phénomène illustre-t-il ? (3 pts)"},
  {"type":"step","label":"3","content":"À partir du document 3, explique la relation entre le flux thermique et l'âge de la lithosphère océanique. (2 pts)"},
  {"type":"step","label":"4","content":"Synthèse : en t'aidant des documents, explique le mécanisme de subduction et son rôle dans la formation des chaînes de montagnes. (3 pts)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"PARTIE 3 : Exploitation de documents (5 points)"},
  {"type":"text","content":"Document 4 : Schéma d'une dorsale océanique avec les âges des basaltes (symétrie)."},
  {"type":"text","content":"Document 5 : Carte des anomalies magnétiques de part et d'autre de la dorsale médio-atlantique."},
  {"type":"step","label":"1","content":"Montre comment la symétrie des âges des basaltes prouve l'accrétion océanique. (2 pts)"},
  {"type":"step","label":"2","content":"Explique le principe des anomalies magnétiques et leur rôle dans la datation des fonds océaniques. (3 pts)"},
  {"type":"separator","content":""},
  {"type":"box","content":"📝 À NOTER : Ce sujet est typique du BAC marocain. Les documents sont toujours à analyser précisément.","color":"orange"},
  {"type":"wa
…[tronqué]
```

---

## 4. A4 • LIBRE — exercice BAC SVT (consommation matière organique)

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **SVT**
- **Temps LLM** : 11.4s  •  **Réponse** : 2474 chars

**Message envoyé :** > Exercice BAC SVT sur la consommation de la matière organique : respiration cellulaire, glycolyse, cycle de Krebs.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `respiration cellulaire glycolyse cycle de Krebs ATP mitochondrie`
- **Texte avant le tag (400 derniers chars)** :
  > ent":"Bilan ATP : Glycolyse (2) + Krebs (2) + Chaîne respiratoire (34) = 38 ATP par glucose. Rendement ≈ 40% — le reste est perdu en chaleur.","color":"orange"}
]}}]}</ui>

Maintenant, testons-toi avec une **vraie question du BAC** sur ce thème. Essaie de répondre avant de regarder la correction !

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='respiration cellulaire glycolyse cycle de Krebs ATP mitochondrie') = SVT
- final: subject_hint=SVT (from_user=True)
- **➡ Matière finale : 'SVT'**

### Exercice retourné par exam_bank
- **subject** : `SVT`
- **exam_label** : SVT 2020 Rattrapage
- **exercise_name** : Exercice 1
- **topic** : Consommation de la matière organique et flux d'énergie
- **# questions** : 1

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | contenu : 'respiration cellulaire glycolyse cycle de Krebs ATP mitochondrie' |
| 2 | Matière résolue == SVT (accent-insensitive) | ✅ PASS | résolu : 'SVT' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en SVT (bug original : SVT → PC) | ✅ PASS | subject='SVT', exam='SVT 2020 Rattrapage', topic="Consommation de la matière organique et flux d'énergie" |

### Réponse LLM (2474 chars — extrait)
```
# Exercice BAC SVT — Consommation de la matière organique

Excellent choix ! Le **Domaine 1** représente **25% de l'examen SVT** (coefficient 5). C'est un sujet qui tombe **chaque année** au BAC. Travaillons-le ensemble.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Consommation matière organique — Respiration cellulaire","lines":[
  {"type":"title","content":"🎯 Rappel : Respiration cellulaire (aérobie)"},
  {"type":"text","content":"Équation bilan : $C_6H_{12}O_6 + 6O_2 \\rightarrow 6CO_2 + 6H_2O + 36\\!-\\!38\\,ATP$"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📌 Les 3 étapes clés"},
  {"type":"step","label":"1","content":"Glycolyse — Cytoplasme : Glucose → 2 Pyruvate + 2 ATP + 2 NADH"},
  {"type":"step","label":"2","content":"Cycle de Krebs — Matrice mitochondriale : Pyruvate → CO₂ + NADH + FADH₂ + 2 ATP"},
  {"type":"step","label":"3","content":"Chaîne respiratoire — Membrane interne : NADH/FADH₂ → H₂O + 34 ATP (phosphorylation oxydative)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"⚠️ Piège BAC fréquent"},
  {"type":"warning","content":"Ne confonds PAS : Glycolyse = cytoplasme (pas mitochondrie !). Le cycle de Krebs = matrice mitochondriale. La chaîne respiratoire = membrane interne."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📝 À NOTER ABSOLUMENT"},
  {"type":"box","content":"Bilan ATP : Glycolyse (2) + Krebs (2) + Chaîne respiratoire (34) = 38 ATP par glucose. Rendement ≈ 40% — le reste est perdu en chaleur.","color":"orange"}
]}}]}</ui>

Maintenant, testons-toi avec une **vraie question du BAC** sur ce thème. Essaie de répondre avant de regarder la correction !

<exam_exercise>respiration cellulaire glycolyse cycle de Krebs ATP mitochondrie</exam_exercise>

Après avoir fait l'exercice, dis-moi comment tu t'en es sorti et je t'expliquerai les points qui bloquent. 💪

<suggestions>[
  {"label":"✅ J'ai réussi l'exercice","prompt":"J'ai réussi l'exercice sur la respiration cellulaire, je peux passer à la suite","icon":"✅"},
  {"label":"❌ Je n'ai pas compris","prompt":"Je n'ai pas compris l'exercice sur la respiration cellulaire, réexplique-moi","icon":"❌"},
  {"label":"📝 Donne-moi un autre exercice","prompt":"Donne-moi un autre exercice BAC sur la respiration cellulaire","icon":"📝"},
  {"label":"🔄 Revoir le cours","prompt":"Je veux revoir le cours sur la respiration cellulaire en détail","icon":"🔄"}
]</suggestions>
```

---

## 5. B1 • COACHING SVT — exercice BAC sur génétique

- **Mode** : `coaching`
- **ctx.subject** : `SVT`
- **Matière demandée** : **SVT**
- **Chapitre** : Génétique humaine — transmission de deux gènes
- **Leçon** : Brassage interchromosomique
- **Temps LLM** : 5.7s  •  **Réponse** : 846 chars

**Message envoyé :** > Donne-moi un exercice BAC sur la génétique mendélienne, monohybride ou dihybride, pour m'entraîner.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `(vide)`

### Résolution de matière (trace)
- step1: ctx.subject = 'SVT'
- step1c: kept as explicit (subject_from_user=True)
- final: subject_hint=SVT (from_user=True)
- **➡ Matière finale : 'SVT'**

### Exercice retourné par exam_bank
- **subject** : `SVT`
- **exam_label** : SVT 2025 Rattrapage
- **exercise_name** : Exercice 3
- **topic** : Génétique des populations
- **# questions** : 2

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | (aucun tag — la prod tombera sur force_exam_panel) |
| 2 | Matière résolue == SVT (accent-insensitive) | ✅ PASS | résolu : 'SVT' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en SVT (bug original : SVT → PC) | ✅ PASS | subject='SVT', exam='SVT 2025 Rattrapage', topic='Génétique des populations' |

### Réponse LLM (846 chars — extrait)
```
واخا خويا! دابا غادي نعطيك تمرين ديال BAC على ال dihybridisme، باش تشوف واش فهمتي هاد la partie. هاد التمرين قريب من لي طاح فـ 2023 normale.

هاد التمرين فيه جوج صفات: شكل البذور (Lisse R vs Ridé r) ولونها (Jaune J vs Vert v). J و L سائدين.

**Énoncé :**
On croise une plante de lignée pure à graines [Jaunes, Lisses] avec une plante de lignée pure à graines [Vertes, Ridées]. La génération F1 obtenue est uniforme. On croise ensuite deux plantes de la F1 entre elles. La F2 obtenue compte 320 graines.

1.  Détermine les génotypes des parents et de la F1.
2.  Donne la nature et les proportions des gamètes produits par la F1.
3.  Réalise l'échiquier de croisement F1 × F1.
4.  Donne les proportions phénotypiques et génotypiques de la F2.
5.  Calcule le nombre de graines [Jaunes, Lisses] attendues dans la F2.

حاول تحل التمرين، واش باغي تبدأ؟
```

---

## 6. C1 • LIBRE — exercice BAC Maths (complexes) [contrôle]

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **Mathematiques**
- **Temps LLM** : 12.0s  •  **Réponse** : 2476 chars

**Message envoyé :** > Je veux un exercice BAC en Mathématiques sur les nombres complexes, module argument, équation.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `(vide)`

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='') = None
- step3: _detect_subject_from_text(pre_text len=0) = None
- step4: _infer_subject_from_context() = Mathématiques
- final: subject_hint=Mathématiques (from_user=False)
- **➡ Matière finale : 'Mathématiques'**

### Exercice retourné par exam_bank
- **subject** : `Mathematiques`
- **exam_label** : Mathematiques 2020 Normale
- **exercise_name** : Exercice 2 — Nombres complexes
- **# questions** : 9

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | (aucun tag — la prod tombera sur force_exam_panel) |
| 2 | Matière résolue == Mathematiques (accent-insensitive) | ✅ PASS | résolu : 'Mathématiques' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en Mathematiques (bug original : SVT → PC) | ✅ PASS | subject='Mathematiques', exam='Mathematiques 2020 Normale', topic='Exercice 2 — Nombres complexes' |

### Réponse LLM (2476 chars — extrait)
```
Je te propose un exercice type BAC sur les nombres complexes, niveau 2BAC PC. Prends ton cahier et suis les étapes.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Exercice BAC — Nombres complexes","lines":[{"type":"title","content":"📝 Exercice type BAC — Nombres complexes (module, argument, équation)"},{"type":"separator","content":""},{"type":"subtitle","content":"Énoncé (extrait sujet national)"},{"type":"text","content":"On considère dans $\\mathbb{C}$ l'équation : $z^2 - 2\\sqrt{3}z + 4 = 0$"},{"type":"step","label":"1","content":"Résoudre dans $\\mathbb{C}$ l'équation $(E)$. Donner les solutions sous forme algébrique."},{"type":"step","label":"2","content":"Écrire chaque solution sous forme trigonométrique (module et argument)."},{"type":"step","label":"3","content":"Soit $z_1 = \\sqrt{3} + i$ et $z_2 = \\sqrt{3} - i$. Calculer $\\frac{z_1}{z_2}$ et donner le résultat sous forme algébrique puis trigonométrique."},{"type":"separator","content":""},{"type":"box","content":"⏱️ Temps conseillé : 15 min | Poids BAC : ~20% de l'épreuve | Coefficient Maths : 7","color":"orange"},{"type":"separator","content":""},{"type":"subtitle","content":"💡 Rappels utiles"},{"type":"text","content":"• Discriminant : $\\Delta = b^2 - 4ac$"},{"type":"text","content":"• Si $\\Delta < 0$ : $z = \\frac{-b \\pm i\\sqrt{-\\Delta}}{2a}$"},{"type":"text","content":"• Module : $|a+ib| = \\sqrt{a^2+b^2}$"},{"type":"text","content":"• Argument : $\\cos\\theta = \\frac{a}{|z|}$, $\\sin\\theta = \\frac{b}{|z|}$"},{"type":"separator","content":""},{"type":"warning","content":"⚠️ Piège fréquent : Ne pas oublier le $i$ devant $\\sqrt{-\\Delta}$ quand $\\Delta < 0$ !"},{"type":"separator","content":""},{"type":"tip","content":"✅ Règle d'or : Toujours vérifier que $|z_1| = |z_2|$ pour les solutions conjuguées."}]}}]}</ui>

Maintenant, essaie de résoudre les questions 1, 2 et 3. Je te guide pas à pas. Quelle question veux-tu commencer ?

<suggestions>[
  {"label":"Question 1 : Résoudre (E)","prompt":"Je veux commencer par la question 1 : résoudre l'équation dans C","icon":"🔢"},
  {"label":"Question 2 : Forme trigo","prompt":"Je veux passer à la question 2 : forme trigonométrique","icon":"📐"},
  {"label":"Question 3 : Calcul quotient","prompt":"Je veux faire la question 3 : calculer z1/z2","icon":"➗"},
  {"label":"Je ne sais pas par où commencer","prompt":"Je ne sais pas par où commencer, aide-moi à démarrer","icon":"🤔"}
]</suggestions>
```

---

## 7. C2 • LIBRE — exercice BAC Physique (RLC) [contrôle]

- **Mode** : `libre`
- **ctx.subject** : `Général`
- **Matière demandée** : **Physique**
- **Temps LLM** : 11.8s  •  **Réponse** : 2428 chars

**Message envoyé :** > Donne-moi un exercice BAC en Physique sur le circuit RLC, oscillations électriques.

### Tag <exam_exercise> émis par le LLM
- **Contenu du tag** : `(vide)`

### Résolution de matière (trace)
- step1: ctx.subject = 'Général'
- step1b: neutralised to None (Général)
- step2: _detect_subject_from_text(exam_query='') = None
- step3: _detect_subject_from_text(pre_text len=0) = None
- step4: _infer_subject_from_context() = Physique
- final: subject_hint=Physique (from_user=False)
- **➡ Matière finale : 'Physique'**

### Exercice retourné par exam_bank
- **subject** : `Physique-Chimie`
- **exam_label** : Physique-Chimie 2016 Normale
- **exercise_name** : Exercice III — Physique : Dipôle RC et circuit RLC
- **# questions** : 11

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ℹ️ Tag <exam_exercise> émis (informationnel — fallback en prod) | ✅ PASS | (aucun tag — la prod tombera sur force_exam_panel) |
| 2 | Matière résolue == Physique (accent-insensitive) | ✅ PASS | résolu : 'Physique' |
| 3 | exam_bank a retourné au moins un exercice | ✅ PASS | 1 exercice(s) |
| 4 | ⭐ L'exercice retourné est en Physique (bug original : SVT → PC) | ✅ PASS | subject='Physique-Chimie', exam='Physique-Chimie 2016 Normale', topic='Exercice III — Physique : Dipôle RC et circuit RLC' |

### Réponse LLM (2428 chars — extrait)
```
# Exercice BAC Physique — Circuit RLC (Oscillations électriques)

Très bon choix ! Le circuit RLC fait partie du sous-domaine **Électricité (21% de l'épreuve de Physique)**. C'est un sujet qui tombe **très souvent** au BAC, généralement sous forme d'étude de courbes et de calculs de grandeurs caractéristiques.

Voici un exercice typique du BAC :

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Exercice BAC — Circuit RLC série","lines":[
  {"type":"title","content":"🔌 Circuit RLC série — Oscillations électriques libres"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📋 Énoncé"},
  {"type":"text","content":"On considère un circuit RLC série comprenant :\n• Un condensateur de capacité $C = 10\\,\\mu\\text{F}$ initialement chargé sous une tension $U_0 = 12\\,\\text{V}$\n• Une bobine d'inductance $L = 0,1\\,\\text{H}$ et de résistance $r$ négligeable\n• Un conducteur ohmique de résistance $R$ variable"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"❓ Questions"},
  {"type":"step","label":"1","content":"Établir l'équation différentielle vérifiée par la charge $q(t)$ du condensateur."},
  {"type":"step","label":"2","content":"Exprimer la pulsation propre $\\omega_0$ et la période propre $T_0$ des oscillations."},
  {"type":"step","label":"3","content":"Calculer $T_0$ et la fréquence propre $f_0$."},
  {"type":"step","label":"4","content":"Donner l'expression de $q(t)$ sachant qu'à $t=0$, $q(0)=Q_0$ et $i(0)=0$."},
  {"type":"step","label":"5","content":"Exprimer l'énergie totale $E$ du circuit. Que devient cette énergie si $R \\neq 0$ ?"},
  {"type":"separator","content":""},
  {"type":"box","content":"💡 Rappel : $i = \\frac{dq}{dt}$ et $u_C = \\frac{q}{C}$","color":"green"}
]}}]}</ui>

---

**Essaie de répondre aux questions 1, 2 et 3 d'abord.** Je te guiderai étape par étape si tu bloques. Prends une feuille et lance-toi !

<suggestions>[
  {"label":"Je commence la Q1","prompt":"Je veux essayer la question 1, établir l'équation différentielle","icon":"✏️"},
  {"label":"Je bloque sur Q1","prompt":"Aide-moi à démarrer la question 1, je ne sais pas par où commencer","icon":"🤔"},
  {"label":"Donne la correction","prompt":"Donne-moi directement la correction complète de l'exercice","icon":"📖"},
  {"label":"Un autre exercice","prompt":"Propose-moi un autre exercice BAC sur un thème différent","icon":"🔄"}
]</suggestions>
```

---

**Score final : 28/28** — 🎉 TOUT VERT
